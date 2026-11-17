---
name: arknights-garrison-s1-skill
description: 明日方舟「卫戍协议·规程·序列Ⅰ」离线数据与攻略：26 个盟约效果、155 名干员的卫戍能力/技能、认证与关键目标数值、叠层与阵容协同。Use when asked about Arknights Stronghold Protocol / 卫戍协议 / 自走棋 规程 序列I：盟约怎么叠、某个干员带哪个技能、乌萨斯/灵巧/奥术等阵容怎么搭、认证/兑换收益。
---

# 卫戍协议·规程·序列Ⅰ

赛季 `act3autochess-v3_1`（2026-11-08 开放，常驻赛季化第一季）。所有结论先查本 skill 的数据库，不要凭记忆。

## 数据文件

| 文件 | 内容 |
|---|---|
| `data/garrison.db` | SQLite：`operators` / `bonds` / `operator_bonds` / `garrisons` / `bands` / `choices` / `items`、视图 `v_ops` |
| `data/operators.csv` | 155 名干员（等阶/星级/职业/盟约/基础与精锐能力/技能） |
| `data/bonds.csv` | 26 个盟约（10 核心 + 16 附加，激活人数、阈值、效果全文） |
| `data/operator_bonds.csv` | 干员-盟约 多对多 |
| `references/covenants.md` | 盟约总表 + 每个盟约的所属干员清单 |
| `references/operators.md` | 按等阶排列的全部干员（含卫戍能力基础/精锐） |
| `references/season-1.md` | 赛季机制：模式、认证、关键目标、兑换、阶段与时间线 |
| `references/synergy.md` | 阵容协同：乌萨斯、灵巧、双盟约桥、8 人口骨架 |

## 查询

```bash
python3 scripts/query.py op 奥尔佳
python3 scripts/query.py bond 乌萨斯
python3 scripts/query.py tier 6
python3 scripts/query.py search 术师
python3 scripts/query.py sql "select name,bonds from operators where bond_ids like '%lethaniaShip%'"
```

或直接 `sqlite3 data/garrison.db`。`operators.bonds`/`bond_ids` 用 `|` 分隔；`ability_base`/`ability_elite` 是基础/精锐（金卡）两档。

## 回答套路

1. **先查库**：技能名、SP、数值、盟约归属都以 DB/`references` 为准；技能数值分 4 级（基础）与 7 级（精锐）。
2. **看卫戍能力的触发方式**：`获得时`（一次性）/`战斗开始时`/`每次开启技能`（吃 SP 与持续）/`休整期结束时`（每回合产层）/`作战能力`（吃层数的输出）。叠层问题必须算“每回合产量 vs 每回合上限”。
3. **技能选择**看三点：SP 与持续时间（覆盖率）、是否触发自身卫戍能力、是否服务团队。自动回复约 1 SP/s。
4. **阵容给 8 人口骨架**（单人模拟上场上限 8），并说明每个位置换人条件。
5. 核心盟约 3 人激活（阈值 3/6），附加盟约多数 2 人；双盟约干员是压缩人口的钥匙。

## 维护

- 数据版本与上游仓库见 `references/season-1.md`；换赛季时替换 `data/` 并按新 `VERSION` 重新生成 `references/covenants.md`、`references/operators.md`。
- 隐藏项（2 名隐藏、14 名 `visible=false`）也在库中，`operators.is_hidden` / `operators.visible` 可过滤。
