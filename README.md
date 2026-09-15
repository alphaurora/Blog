# Alpha Journal

Apple 官网风格启发的个人博客：黑白主色、宽阔留白、大字号排版，适配手机与桌面，支持明暗主题自由切换并记住选择。没有使用 Apple 商标或素材。仓库附带三篇示例文章，可替换为自己的内容。

## 写文章

在 `content/` 新增 `.md` 文件，文件名使用英文短横线形式。每篇文章以以下元信息开头：

```markdown
---
title: 你的文章标题
date: 2026-09-15
category: 技术笔记
description: 一句话介绍文章。
---

## 正文标题

支持 **粗体**、列表、引用、链接、图片、代码块和表格。
```

最新日期的文章会自动显示在首页精选位置。编辑 `site.json` 修改博客名称、首页标题、描述和 GitHub 地址。

## 本地生成与预览

需要 Python 3.10 或更新版本：

```sh
python3 -m pip install -r requirements.txt
python3 build.py
python3 -m http.server 8000 --directory dist
```

打开 http://localhost:8000 。生成后的 `dist/` 可直接托管，阅读不依赖浏览器 JavaScript。文章链接采用相对路径，支持子目录部署。

文章只应由仓库维护者编辑；Markdown 允许内嵌 HTML，不接受匿名访客上传。

## GitHub 更新

包含自动生成流程：提交 `content/`、`site.json`、`build.py` 后，GitHub Actions 会重建并提交静态网页。流程需要仓库允许 Actions 写入内容。Sites 版本需再次发布后才会更新线上网页。
