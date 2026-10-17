---
name: win-desktop-xlsx-safe-edit
description: "Safe end-to-end workflow for editing an EXISTING .xlsx that lives on the Windows Desktop (or another live user folder) of this machine: backup → openpyxl style-preserving edit → UTF-8 JSON verification (avoids Git Bash GBK mojibake) → ~$ lock check, and when the file is locked by Excel/WPS (Device or resource busy) deliver via outputs first and write back after the user closes it. Use when 用户要求修改/完善桌面上已有的中文 xlsx（投标参数表、应用场景表、明细表等）、向用户目录写回文件、在 Git Bash 中校验中文内容，或 cp 报 Device or resource busy 时。与 xlsx 技能叠加使用：内容/公式/格式规范看 xlsx，文件系统安全流程看本技能。"
version: 1.0.0
---

# Windows 桌面 xlsx 安全编辑

与 `xlsx` 技能分工：xlsx 技能管"怎么把表格内容做好"（公式、格式、重算），本技能管"在用户真实使用中的文件上安全落地"（备份、防占用、中文校验）。两者同时适用时：内容遵循 xlsx 技能，文件操作流程遵循本技能。

## 适用场景

- 就地修改桌面/文档/其他用户目录下**已存在**的中文 xlsx（不是新建文件交付）
- 目标文件可能正被 Excel/WPS 打开
- 需要在 Git Bash 控制台下校验中文内容或样式

## 工作流总览

| 步骤 | 动作 | 要点 |
|---|---|---|
| 0 | 环境 | `uv run --with openpyxl python` 跑脚本，一切操作先在工作区副本上进行 |
| 1 | 预检+备份 | 查 `~$` 锁文件；`cp` 原文件到工作区为 `xxx_orig.xlsx`，全程保留 |
| 2 | 样式探测 | openpyxl dump 字体/边框/对齐/列宽为 UTF-8 JSON，用 Read 看 |
| 3 | 保样式写入 | 编辑工作区副本，继承原样式，长文本列加自动换行与列宽 |
| 4 | 中文校验 | `json.dump(ensure_ascii=False)` 落盘后 Read，**永远不信控制台中文输出** |
| 5 | 写回/降级 | `cp` 写回原位置；busy 则存 outputs 交付，待用户关闭后再写回 |

## 步骤 0：环境约定

本机 python 不在 PATH，一律 `uv run --with openpyxl python` 执行脚本（需要 Excel COM 时加 `--with openpyxl,pywin32`）。当前会话工作区（workspace）作为唯一作业区，**绝不直接编辑用户目录里的原文件**。

## 步骤 1：预检与备份

```bash
ls "/c/Users/<用户名>/Desktop/" | grep -i "~\$"          # 检查锁文件
cp "/c/Users/<用户名>/Desktop/文件.xlsx" "<工作区>/文件_orig.xlsx"   # 备份
```

- 存在 `~$文件.xlsx`：文件正被 Excel/WPS 编辑，写回大概率失败 → 提前按步骤 5 的降级路径准备。
- **没有 `~$` 不等于未占用**：WPS 可能不建锁文件，cp 仍可能报 `Device or resource busy`。一切以 cp 结果为准。
- 备份文件 `文件_orig.xlsx` 全程保留，是出错回滚的最后保障；任务成功交付前不得删除。

## 步骤 2：样式探测（先 dump 再看）

编辑前先弄清原表的字体、边框、对齐、列宽、合并单元格，避免写入后风格走样：

```bash
uv run --with openpyxl python << 'EOF'
import openpyxl, json
wb = openpyxl.load_workbook('文件_orig.xlsx')
ws = wb.active
info = {'col_widths': {k: v.width for k, v in ws.column_dimensions.items()},
        'merged': [str(r) for r in ws.merged_cells.ranges]}
cells = {}
for row in ws.iter_rows():
    for c in row:
        if c.value is not None:
            cells[c.coordinate] = {'v': c.value, 'font': c.font.name,
                'size': c.font.sz, 'border_l': c.border.left.style,
                'wrap': c.alignment.wrap_text, 'align_h': c.alignment.horizontal}
with open('style.json', 'w', encoding='utf-8') as f:
    json.dump({'info': info, 'cells': cells}, f, ensure_ascii=False, indent=1, default=str)
EOF
```

然后用 Read 工具读 `style.json`。典型样式基准（本机投标/参数表常见）：宋体 11、四边细边框、表头居中、内容列自动换行 + 垂直居中。

## 步骤 3：保样式写入

只编辑工作区副本：

- **继承原样式**：新写单元格沿用同行/同列的字体（如宋体）、边框（thin）、对齐。`insert_cols` 后新列样式不会自动跟随，用 `from copy import copy` 从相邻列复制 `font`/`border`/`alignment`。
- **长文本列**：`Alignment(wrap_text=True, vertical='center')`，并加宽列宽（如 `ws.column_dimensions['C'].width = 68`），否则内容挤成一条线。
- **合并单元格只写左上锚点**，其余格是只读 MergedCell。
- **严禁 `load_workbook(..., data_only=True)` 后保存**：公式会被永久替换成字面量。读取缓存值做分析时用 `data_only=True`，写入编辑用默认模式，两个工作簿对象分开。
- 需要插入行/列时注意表头与序号列联动，改完整体 dump 校验。

## 步骤 4：中文校验（规避 GBK 乱码）

Git Bash 控制台是 GBK 码页，python `print` 的中文会显示为乱码。**控制台乱码 ≠ 文件内容错误**，也不要靠控制台核对中文——标准动作是落盘 UTF-8 JSON 再用 Read 工具看：

```bash
uv run --with openpyxl python << 'EOF'
import openpyxl, json
wb = openpyxl.load_workbook('文件.xlsx')
ws = wb.active
rows = []
for r in range(1, ws.max_row + 1):
    rows.append({c: ws.cell(row=r, column=i).value for i, c in enumerate('ABCD', 1)})
with open('verify.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=1, default=str)
EOF
```

- 用 Read 工具核对单元格内容与样式字段（wrap、font 等），逐行确认后再进入写回。
- 报错信息若含中文路径，同样重定向到文件后 Read，避免乱码干扰判断。

## 步骤 5：写回与占用降级

```bash
cp "<工作区>/文件.xlsx" "/c/Users/<用户名>/Desktop/文件.xlsx" && ls -la "/c/Users/<用户名>/Desktop/文件.xlsx"
```

- **写回成功**：完成；若之前交付过 outputs 副本，同步更新该副本。
- **报 `Device or resource busy`**（文件被 Excel/WPS 打开）：
  1. 把结果存入会话 `outputs/` 目录，用 `present_files` 交付；
  2. 明确告知用户：桌面原文件被占用未能写回，请关闭该文件后告知，我立即写回原位置；
  3. 用户回复已关闭后，重新检查 `~$` 并再次 `cp` 写回，然后确认 `ls -la` 时间戳。
- **outputs 副本也可能被占用**：用户可能正打开着上一版交付文件，同名覆盖同样报 busy → 换新文件名输出（如附加本次改动的语义后缀），不要反复重试同名文件。
- 整个降级期间工作区备份与成品副本都保留，写回永远是"副本覆盖"，不是现场编辑。

## 公式处理（如适用）

本机没有 LibreOffice，xlsx 技能的 `formula_refresh.py` 不可用。含公式的文件需要重算时改用 Excel COM：

```bash
uv run --with openpyxl,pywin32 python << 'EOF'
import win32com.client as wc
app = wc.Dispatch('Excel.Application')
wb = app.Workbooks.Open(r'C:\绝对路径\文件.xlsx')
app.CalculateFullRebuild()
wb.Save(); wb.Close(); app.Quit()
EOF
```

注意 COM 打开期间文件同样被占用，写回顺序应为：openpyxl 编辑 → COM 重算保存 → 再交付/写回。

## Pitfalls

- 无 `~$` 锁文件 ≠ 未被占用，一切以 `cp` 是否报 busy 为准。
- Git Bash 控制台中文必乱码（GBK），文件本身没问题，不要因此"修复"内容。
- `data_only=True` 读取的工作簿保存后公式永久丢失。
- `insert_cols` 新列样式为空，必须手动从相邻列复制。
- 禁止永久删除备份与用户原文件；回滚依赖工作区备份。
- 用户对"写回桌面"有明确预期时，降级交付必须主动说明，不能只丢一个 outputs 文件。

## Verification

1. `verify.json` 经 Read 逐行核对，内容与样式字段全部符合预期（不看控制台）。
2. 写回成功后 `ls -la` 确认目标文件大小/时间戳已更新。
3. 若发生降级交付：outputs 文件存在且已 `present_files`，回复中已告知用户待办（关闭文件后写回）。
4. 交付说明中写清本次改动点与遗留事项（如尚未写回的原文件路径）。
