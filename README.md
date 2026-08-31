# Grok Bot 中文目录

独立社区的 [grokbot.dev](https://grokbot.dev/) 简体中文本地化。即用提示词、插件、合集与可分享机器人。由 CRHQ 原站内容译出，**不隶属于 xAI**。

- 代码：MIT（见 LICENSE）
- 内容：CC BY 4.0（见 LICENSE-CONTENT.md）——复用任何条目必须同时署明该条作者和 grokbot.dev（名字 + 链接）

## 运行

需要 Node 22（Node 20 亦可构建）。

```bash
cd /workspace/grokbot-zh
npm install
npm run dev      # http://localhost:4380
npm run build
```

数据快照在 data/source/。中文目录生成在 data/localized/。

## 页面

- / 首页
- /plugins 与插件详情
- /marketplace 307 只可分享机器人（筛选+中英搜索）
- /use-cases 138 条精选用例
- /collections 合集
- /categories 与 /integrations
- /about /privacy /submit /contribute
- /agent 中文例程，指向原文 API
- /plugin-builder
- 中文 404

提示词保持英文。原帖只引用，不整篇转载。
