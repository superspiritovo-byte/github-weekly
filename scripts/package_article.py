"""Package a five-project illustrated article. Standard library only; no network."""
import argparse
import base64
import html
import json
import mimetypes
import shutil
import zipfile
from pathlib import Path
from urllib.parse import urlparse

OPENING = 'Hello，大家好！'
CLOSING = '记得点赞、收藏、关注。'


def text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Required text is empty')
    return value.strip()


def package(source, output):
    data = json.loads(source.read_text(encoding='utf-8-sig'))
    title, intro = text(data.get('title')), text(data.get('intro'))
    projects, images = data.get('projects', []), data.get('images', [])
    if len(projects) != 5 or len(images) != 3:
        raise ValueError('Exactly five projects and three images are required')
    for p in projects:
        for key in ('name', 'what', 'who', 'difficulty', 'url'):
            p[key] = text(p.get(key))
        u = urlparse(p['url'])
        if u.scheme != 'https' or u.netloc != 'github.com' or len(u.path.strip('/').split('/')) < 2:
            raise ValueError('Use HTTPS GitHub repository addresses')
    ready = []
    for i, image in enumerate(images):
        path = (source.parent / image['path']).resolve()
        mime = mimetypes.guess_type(path.name)[0]
        before = image.get('before', 0)
        if mime not in ('image/png', 'image/jpeg', 'image/webp') or not path.is_file():
            raise ValueError(f'Unsupported or missing image: {path}')
        if type(before) is not int or not 0 <= before < 5:
            raise ValueError('Image before must be an integer from 0 to 4')
        ready.append((path, mime, before, text(image.get('caption')), f'images/{i+1:02d}{path.suffix.lower()}'))
    if output.exists() and any(output.iterdir()):
        raise ValueError('Choose an empty output directory to avoid overwriting')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'images').mkdir()
    esc = html.escape
    blocks = [f'<h1>{esc(title)}</h1>', f'<p>{OPENING}</p>', f'<p>{esc(intro)}</p>']
    markdown = [f'# {title}', OPENING, intro]
    for i, p in enumerate(projects):
        for path, mime, before, caption, target in ready:
            if before == i:
                shutil.copy2(path, output / target)
                encoded = base64.b64encode(path.read_bytes()).decode('ascii')
                blocks.append(f'<figure><img src="data:{mime};base64,{encoded}" alt="{esc(caption)}"><figcaption>{esc(caption)}</figcaption></figure>')
                markdown += [f'![{caption}]({target})', caption]
        heading = f'{i+1:02d}  {p["name"]}'
        blocks.append(f'<section><h2>{esc(heading)}</h2>')
        markdown.append(f'## {heading}')
        for key in ('what', 'who', 'difficulty'):
            value = ('难度：' if key == 'difficulty' else '') + p[key]
            cls = ' class="difficulty"' if key == 'difficulty' else ''
            blocks.append(f'<p{cls}>{esc(value)}</p>')
            markdown.append(value)
        url = p['url']
        blocks.append(f'<p class="address">地址：<a href="{esc(url, quote=True)}">{esc(url)}</a></p></section>')
        markdown.append(f'地址：[{url}]({url})')
    blocks.append(f'<p>{CLOSING}</p>')
    markdown.append(CLOSING)
    css = '''*{box-sizing:border-box}body{margin:0;background:#f6f7f9;color:#1f2329;font-family:"Microsoft YaHei","PingFang SC",sans-serif}article{max-width:850px;margin:32px auto;padding:48px 52px;background:white;border-radius:12px}h1{font-size:30px;line-height:1.4;margin:0 0 26px}h2{font-size:24px;margin:30px 0 6px}p{font-size:16px;line-height:1.9;margin:12px 0}figure{margin:26px 0}img{display:block;width:100%;height:auto;border-radius:8px}figcaption{color:#7b8290;font-size:12px;margin-top:8px}.difficulty{background:#f4f6fa;border-radius:6px;padding:12px 16px}.address{font-size:14px;overflow-wrap:anywhere}a{color:#245bba;text-decoration:none}section{margin-bottom:26px}@media(max-width:600px){article{margin:0;padding:26px 22px;border-radius:0}h1{font-size:26px}h2{font-size:22px}}'''
    page = f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{css}</style></head><body><article>{"".join(blocks)}</article></body></html>'
    (output / 'article.html').write_text(page, encoding='utf-8')
    (output / 'article.md').write_text('\n\n'.join(markdown) + '\n', encoding='utf-8')
    if data.get('image_generation_notes'):
        (output / 'image-prompts.txt').write_text(data['image_generation_notes'], encoding='utf-8')
    with zipfile.ZipFile(output / 'feishu-article-assets.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(output.rglob('*')):
            if file.is_file() and file.suffix != '.zip':
                archive.write(file, file.relative_to(output))
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(package(args.source.resolve(), args.out.resolve()))
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.error(str(error))
