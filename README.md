<h1 align="center">Grok Bot 中文目录</h1>

<p align="center">独立社区的 grokbot.dev 简体中文本地化版本，收录即用提示词、插件、精选用例与可分享机器人。</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/Code%20License-MIT-22C55E?style=flat-square" alt="Code License: MIT"></a>
  <a href="./LICENSE-CONTENT.md"><img src="https://img.shields.io/badge/Content%20License-CC%20BY%204.0-22C55E?style=flat-square" alt="Content License: CC BY 4.0"></a>
  <img src="https://img.shields.io/badge/Node.js-%3E%3D20-3776AB?style=flat-square" alt="Node.js: >=20">
  <img src="https://img.shields.io/badge/Astro-5.x-4F46E5?style=flat-square" alt="Astro: 5.x">
</p>

Grok Bot 中文目录是基于 [grokbot.dev](https://grokbot.dev/) 的独立社区简体中文本地化项目。通过精细化的人工校对与脚本管线，将原站收录的 300+ 机器人、100+ 用例及插件生态完整汉化，为中文开发者与创作者提供快速检索与参考工具。

> [!NOTE]
> 本项目为独立社区维护，**不隶属于 xAI**。提示词（Prompts）保持英文原文以避免影响机器人生成效果；原帖均通过链接引用，不整篇转载。

## 核心特性

| 特性 | 说明 | 对应页面 |
|---|---|---|
| 机器人市场 | 收录 300+ 可分享机器人，支持中英双语检索与分类过滤 | `/marketplace` |
| 插件与集成 | 覆盖官方与第三方插件详情、参数说明与配置方式 | `/plugins`, `/integrations` |
| 精选用例库 | 包含 130+ 场景用例，涵盖代码、创意、研究与日常提效 | `/use-cases` |
| 主题合集 | 按工作流与应用场景打包的精选机器人合集 | `/collections` |
| 开发者套件 | 提供中文 API 例程与交互式插件构建器 | `/agent`, `/plugin-builder` |

## 架构与数据流

```text
┌──────────────────┐
│   grokbot.dev    │  (上游快照数据)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   data/source/   │  (原始 JSON 快照)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ scripts/localize │  (Python 本地化处理管线)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ data/localized/  │  (本地化后的中文数据集)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    Astro SSG     │  (静态页面生成与路由系统)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│      dist/       │  (静态站点产物)
└──────────────────┘
```

## 运行环境

- Node.js: `>= 20.0.0` (推荐 Node 22)
- Python: `>= 3.10` (用于数据本地化脚本)
- 包管理器: `npm`

## 快速安装

```bash
git clone https://github.com/245678000000/grokbot-zh.git
cd grokbot-zh
npm install
```

## 快速上手

### 启动本地开发服务

```bash
npm run dev
```

启动后在浏览器中访问 `http://localhost:4380` 查看站点。

### 运行数据本地化脚本

如需根据 `scripts/zh_*.py` 规则重新生成或更新本地化数据：

```bash
npm run localize
```

### 构建静态站点

```bash
npm run build
```

构建生成的静态文件位于 `dist/` 目录中。如需本地预览生产构建产物：

```bash
npm run preview
```

## 项目结构

```text
grokbot-zh/
├── data/
│   ├── source/        # 上游抓取的原始数据快照
│   └── localized/     # 本地化生成的中文数据集
├── scripts/
│   ├── localize.py    # 本地化入口主脚本
│   └── zh_*.py        # 各模块翻译规则与术语映射字典
├── src/
│   ├── components/    # Astro 页面组件
│   ├── layouts/       # 基础页面布局与排版
│   ├── pages/         # 站点路由与页面定义
│   └── styles/        # 样式变量与设计规范
└── public/            # 静态资源与客户端脚本
```

## 贡献指南

欢迎提交 PR 或在 Issues 中反馈翻译建议与新增机器人条目：

1. Fork 本仓库并克隆到本地。
2. 在 `scripts/zh_*.py` 中补充或优化翻译字典。
3. 执行 `npm run localize` 验证数据生成无误。
4. 运行 `npm run build` 确保静态构建通过。
5. 提交 PR 并详细描述变更内容。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=245678000000%2Fgrokbot-zh&type=Date)](https://star-history.com/#245678000000/grokbot-zh&Date)

## 许可证

本项目采用双重授权模式：

- **代码部分**：遵循 [MIT License](./LICENSE) 授权。
- **内容部分**：遵循 [Creative Commons Attribution 4.0 International (CC BY 4.0)](./LICENSE-CONTENT.md) 授权。复用条目时须按照 [LICENSE-CONTENT.md](./LICENSE-CONTENT.md) 注明原作者及 grokbot.dev 来源链接。
