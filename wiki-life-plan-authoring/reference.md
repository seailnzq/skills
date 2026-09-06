# reference.md — wiki-life 库结构与 WIKI-SCHEMA 入库细则

## 定位 vault（跨平台）

`wiki-life` 是用户的私人「内在系统」Obsidian 库，同时是 git 仓库。约定路径 `~/.workbuddy/wiki-life`：

| 环境 | 路径 |
|------|------|
| Windows host | `C:\Users\<user>\.workbuddy\wiki-life` |
| macOS/Linux host | `~/.workbuddy/wiki-life` |
| VM / 容器 | 可能挂载在别处；先探测 |

探测顺序：
1. `ls` 上述约定路径下的 `WIKI-SCHEMA.md` 与 `wiki/`；命中即确认为目标库。
2. 无访问权限 → `mcp__workspace_request_directory` 请求用户选择该 vault 目录。
3. 注意区分：`wiki-knowledge`（对外研报库）与 `wiki-life`（人生库）平行、互不混合。本技能**只操作 wiki-life**；涉及研报同步属 `wps-collection-wiki-sync`。

## 库结构（以库内 WIKI-SCHEMA.md 为准，下面是典型形态）

```
wiki-life/
├── raw/                      # 原始素材，不可变
├── wiki/
│   ├── index.md              # 内容目录
│   ├── log.md                # 操作日志（只追加）
│   ├── overview.md           # 人生系统总纲（中心主题 + 五要素模型）
│   ├── 认知体系与个人画像.md   # 画像底座
│   ├── framework/            # 理论层：第一性原理 / 思维工具 / 心性箴言 / 人生阶段与目标 / 投资纪律 / 投资认知复盘
│   ├── elements/             # 五要素+工作/投资：心与认知 / 身与健康 / 关系 / 价值 / 时间 / 工作 / 投资
│   └── execution/            # 年度实践：养老退休测算 / 医保退休规划 / 持仓假设清单 / 学习输入 / 健康管理 / 关系经营 / 投资记录 / 事项提醒
└── WIKI-SCHEMA.md
```

模型：人生是以「心+认知」为核心的五要素系统（心+认知 / 身 / 关系 / 价值 / 时间）+ 工作、投资两个实践领域。规划文档要挂回这套语言。

## 入库细则（仅在用户明确审定后执行）

1. **归位**：主文档 → `wiki/framework/`（方向层属理论/框架）；附录 → `wiki/synthesis/`（若库无该层，就近并入 framework 并在 log 说明）。文件名去掉"草稿"字样。
2. **frontmatter**：`status` 由「草稿 v0.N 待审（未入库）」改为「已入库 YYYY-MM-DD」；补 `type`（framework / synthesis）。涉及健康数据、财务数字、人名的页面标 `tags: [私密]`。
3. **双链**：一律 `[[...]]`，路径式链接指向库内页（如 `[[framework/人生阶段与目标]]`、`[[elements/关系]]`、`[[execution/持仓假设清单]]`）。要素页↔框架页、要素页↔执行页互链；确保新页被 `index.md` 或 `overview.md` 可达（否则成孤页）。
4. **矛盾/待确认显式标注**：`> ⚠️ 待修正：…` 或 `> ❓ 疑问：…`。
5. **index / log**：更新 `wiki/index.md` 目录条目；在 `wiki/log.md` **追加**（勿改历史）一行：日期 + 变更摘要 + 版本。
6. **git**：`git add <具体文件>`（按名加，勿 `git add -A`）→ `git commit`。库已是 git 仓库，编辑前无需另备份；**远程必须为私有仓库才可 push**（含隐私）。若远程非私有，只 commit 不 push，并提示用户。

## 保密

库含健康、财务、家庭关系隐私。对话与文件中不无谓扩散具体姓名/金额；WebSearch 时不要把疑似私密标识符（真实姓名、账户、保单号）送进搜索引擎，只查公开的政策/产品/宏观参数。
