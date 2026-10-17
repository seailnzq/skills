# 换机恢复包模板（portable/ migration package templates）

本文件是 `awareness-git-sync` 第 9 节的配套模板：给出 `portable/` 五件套的**可复用骨架**。
生成时把 `<...>` 占位替换成实际值，正文中的 PowerShell 片段保持 **ASCII-only**（PS 5.1 用 GBK 读含中文的 .ps1 会报"字符串缺少终止符"）。

放置位置：awareness 镜像库内 `portable/`。

```
awareness/portable/
  RESTORE.md
  bootstrap.ps1
  CRON.md
  SECRETS.manifest.md
  config/mcp.json
```

---

## 1. bootstrap.ps1 骨架（默认 DRY-RUN）

要点：默认只打印；`-Apply` 才写盘；目标已存在则先备份 `.bak-<时间戳>` 永不删除；`mcp.json` 仅当缺失时放置；技能复制排除运行时/索引文件。全文 ASCII。

```powershell
# bootstrap.ps1 - Restore local QwenWork state from the mirrored git repos.
# DEFAULT = DRY RUN. Pass -Apply to actually write.
[CmdletBinding()]
param(
  [string]$ReposRoot = (Split-Path -Parent $PSScriptRoot),  # dir holding awareness/ skills/ ...
  [string]$QwHome    = (Join-Path $env:USERPROFILE '.qwenworkcn'),
  [switch]$Apply
)

$mode = if ($Apply) { 'APPLY' } else { 'DRY-RUN' }
Write-Output "=== bootstrap ($mode)  QwHome=$QwHome ==="

function Copy-Item-Safe($src, $dstRoot) {
  if (-not (Test-Path -LiteralPath $src)) { Write-Output "  SKIP (missing): $src"; return }
  $dst = Join-Path $dstRoot (Split-Path -Leaf $src)
  if (Test-Path -LiteralPath $dst) {
    $bak = "$dst.bak-$(Get-Date -Format yyyyMMddHHmmss)"
    Write-Output "  BACKUP: $dst -> $bak"
    if ($Apply) { Rename-Item -LiteralPath $dst -NewName (Split-Path -Leaf $bak) }
  }
  Write-Output "  COPY  : $src -> $dst"
  if ($Apply) {
    New-Item -ItemType Directory -Force -Path $dstRoot | Out-Null
    Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
  }
}

# 1) awareness human-readable md -> QwHome\awareness\main
$aw = Join-Path $ReposRoot 'awareness'
$awMain = Join-Path $QwHome 'awareness\main'
foreach ($f in 'MEMORY.md','USER.md','AGENTS.md') { Copy-Item-Safe (Join-Path $aw $f) $awMain }
$daily = Join-Path $aw 'memory'
if (Test-Path -LiteralPath $daily) {
  Get-ChildItem -LiteralPath $daily -Filter *.md | ForEach-Object { Copy-Item-Safe $_.FullName (Join-Path $awMain 'memory') }
}

# 2) self-built skill dirs -> QwHome\skills (exclude runtime/index/migration files)
$sk = Join-Path $ReposRoot 'skills'
$skDst = Join-Path $QwHome 'skills'
if (Test-Path -LiteralPath $sk) {
  Get-ChildItem -LiteralPath $sk -Directory | ForEach-Object {
    if ($_.Name -ne '.git') { Copy-Item-Safe $_.FullName $skDst }
  }
}
Write-Output "  NOTE : do NOT restore SKILLS-INDEX.md or *.json migration files into skills/."

# 3) mcp.json -> only if absent (never overwrite existing config)
$mcp = Join-Path $aw 'portable\config\mcp.json'
$mcpDst = Join-Path $QwHome 'mcp.json'
if ((Test-Path -LiteralPath $mcp) -and -not (Test-Path -LiteralPath $mcpDst)) {
  Write-Output "  PLACE: $mcp -> $mcpDst"
  if ($Apply) { Copy-Item -LiteralPath $mcp -Destination $mcpDst }
} else {
  Write-Output "  SKIP : mcp.json (target exists or snapshot missing)"
}

Write-Output "=== MANUAL CHECKLIST (after run) ==="
Write-Output "  [ ] Re-provision credentials / login states -> see SECRETS.manifest.md"
Write-Output "  [ ] Re-enter private ledgers (retirement amounts / stock positions) offline"
Write-Output "  [ ] Recreate scheduled tasks -> see CRON.md (qwenwork.cron)"
if (-not $Apply) { Write-Output "  DRY-RUN only. Re-run with -Apply to write." }
```

生成后**真跑一次**（不带 -Apply）：`powershell -NoProfile -ExecutionPolicy Bypass -File bootstrap.ps1`，确认退出码 0、无语法错误。

---

## 2. RESTORE.md 大纲

```markdown
# RESTORE.md — 换机恢复 SOP（把新机器还原成"感知一致"）

## 0. 前置
- 新装 QwenWork；拿到四个私有库的读权限（见 SECRETS.manifest.md）。

## 1. clone 四库
git clone <awareness>; git clone <skills>; git clone <wiki-life>; git clone <wiki-knowledge>
（放到同一个 ReposRoot 下）

## 2. 跑 bootstrap（先 dry-run 再 -Apply）
powershell -File awareness/portable/bootstrap.ps1            # 预览
powershell -File awareness/portable/bootstrap.ps1 -Apply     # 写入

## 3. 手工补
- 凭据/登录态：按 SECRETS.manifest.md 逐条置备（GitHub PAT、钉钉 DWS、微信 IM…）
- 私密账/金额：私有库允许明文(§8轴①)，clone 回来即自带；仅"助手从未取得"或"别在这台 DLP 机落盘"的部分才留占位，回填到干净机做
- 真实凭据（PAT/API Key/token）：任何 git 都不进，只在密码管理器/登录态
- 定时任务：照 CRON.md 在 QwenWork 里重建（qw_query/cron）

## 4. 验证清单
- MEMORY/USER/AGENTS 与 memory/*.md 到位
- 自研技能出现在 skills/ 且可被加载
- cron 任务按 schedule 正常出现
```

---

## 3. CRON.md 字段表（从 qw_query key=qwenwork.cron 重建，按 §8 两轴处理）

每任务一节，保留"可重建施工图"，**不抄超长 payload**：

```markdown
## <任务名>
- 状态: enabled|disabled
- schedule: <expr + tz>  |  every:<ms>  |  at:<ISO>
- model: <flash|pro|...>（继承默认则写 default）
- 用途: <一句话>
- 依赖: contextDirs=<...>；用到 skill=<...>；投递会话=<名称>
- 骨架 prompt: <意图描述。金额/仓位可明文入私有库(§8轴①)；仅当"助手从未取得该值"或"须避免在本 DLP 机落盘"时才用 {{私密:见线下账}} 占位，回填改到干净机做>
```

> 上市公司名、公开 IPO 参数属公开信息。个股仓位比 / 退休绝对金额：私有库**允许明文**（§8 轴①），不强制占位；只有"我从未从离线账取得"或"这台监控机不宜落盘"时才留占位符，到干净机再补。真实凭据（PAT/API Key/token）才是任何 git 都不进。

---

## 4. SECRETS.manifest.md 结构（只列条目，绝不含值）

```markdown
# SECRETS.manifest — 新机需重新置备的凭据 / 登录态清单

| 条目 | 类型 | 需要的权限 | 备注 |
|---|---|---|---|
| GitHub fine-grained PAT | token | 四个私有库 Contents: Read and write；awareness 需手工加入白名单 | 值仅存本机/密码管理器，不入库 |
| 钉钉 DWS 连接器 | 登录态 | 重新登录授权 | |
| 微信 IM 连接器 | 登录态 | 重新登录授权 | |
| <其它连接器/API Key> | ... | ... | 真实值在应用登录态与环境变量，不在 mcp.json |
```

---

## 5. config/mcp.json 脱敏规则（快照只留结构）

- 保留：server 名称、command、args、type、url 的**主机/路径结构**。
- 清空/占位：任何 `headers.Authorization`、`env` 里的 token/key/secret、query 里内嵌凭据 → 用 `<REDACTED>`。
- 校验：脱敏后对快照跑 `github_pat_|ghp_|sk-|Authorization.*Bearer` grep，期望为空。
- 说明真实值去向（登录态/环境变量）写进 SECRETS.manifest.md 的备注，而非 mcp.json。
