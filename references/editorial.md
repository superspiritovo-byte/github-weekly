# 写稿与图片参考

## 正文骨架

本周 GitHub 热门项目推荐

Hello，大家好！

这期挑了 5 个项目，涵盖〔本期实际领域〕。〔可省略的简短看点。〕

### 01 项目名

〔具体用途和有用之处，别写“革命性”“必备神器”。〕

〔适合什么人，在什么任务或困扰下使用。给一个贴近的场景即可。〕

难度：〔较低／中等／较高〕。〔实际前置条件和限制。〕

地址：〔官方 GitHub 仓库链接〕

其余四个项目同样覆盖这些信息，不必每段开头完全一样。

记得点赞、收藏、关注。

## 配图提示词

每张图分别生成，按实际项目改写方括号内容。

封面：

```text
Use case: illustration-story.
Asset: 16:9 editorial cover for a Chinese GitHub weekly article.
Subject: five miniature objects representing [five actual projects and functions].
Style: tactile paper and clay, warm ivory background, navy and restrained cobalt, soft daylight, clean magazine composition.
Exact headline: 本周 GitHub 热门项目推荐
Subtitle: 5 个值得试试的开源工具
Constraints: readable Chinese; no star counts, rankings, fake product interfaces, endorsements or watermarks.
```

两张正文图分别使用：

```text
Use case: illustration-story.
Asset: 16:9 conceptual editorial illustration.
Subject: [two or three actual projects, represented by concrete objects explaining their purpose].
Style: match the cover's paper and clay texture, ivory, navy and cobalt, soft daylight.
Text: [exact project names only].
Constraints: balanced composition, readable labels, no fake screenshots, statistics, logos or watermarks.
```

提示词本身不代表已指定底层模型。

## 脚本输入

JSON 使用 UTF-8。`projects` 必须有 5 条，以下仅展示其中一条的格式。`images` 必须有 3 条；路径相对 JSON 所在目录解析。`before` 是 0–4 的项目索引，0 表示第一个项目前，1 表示第二个项目前。

```json
{
  "title": "本周 GitHub 热门项目推荐",
  "intro": "自然简短的本期介绍。",
  "projects": [
    {
      "name": "项目名",
      "what": "用途与具体优点。",
      "who": "适用人群与场景。",
      "difficulty": "中等。具体前置条件和限制。",
      "url": "https://github.com/owner/repository"
    }
  ],
  "images": [
    {"path": "cover.png", "before": 0, "caption": "本期封面 · AI 概念插画"},
    {"path": "coding.png", "before": 1, "caption": "概念插画，非产品截图"},
    {"path": "knowledge.png", "before": 3, "caption": "概念插画，非产品截图"}
  ],
  "image_generation_notes": "实际生成方式和三张图的最终提示词，可省略"
}
```

脚本自动插入固定开头和结尾，不要在输入正文中重复。输出目录必须为空或不存在。打开 HTML 检查，不能只检查脚本成功退出。
