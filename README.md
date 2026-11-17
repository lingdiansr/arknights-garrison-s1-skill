# arknights-garrison-s1-skill

明日方舟「卫戍协议·规程·序列Ⅰ」离线数据 + Agent Skill。

包含本赛季全部干员的卫戍能力/技能、26 个盟约的效果与所属干员、认证/关键目标/兑换数值，以及可直接查询的 SQLite 数据库与命令行脚本。作为 Agent Skill 使用时，`SKILL.md` 会被自动发现，回答相关问题前先查本地数据而不是凭记忆。

数据版本：`act3autochess-v3_1`（2026-11-08 开放的「规程·序列Ⅰ」）。

## 内容

| 路径 | 说明 |
|---|---|
| `SKILL.md` | Skill 入口：数据说明、查询方法、回答流程 |
| `data/garrison.db` | SQLite：`operators` / `bonds` / `operator_bonds` / `garrisons` / `bands` / `choices` / `items` |
| `data/operators.csv` | 155 名干员（等阶、星级、职业、价格、盟约、基础/精锐卫戍能力、技能） |
| `data/bonds.csv` | 26 个盟约（10 核心 + 16 附加，激活人数、阈值、效果全文） |
| `data/operator_bonds.csv` | 干员-盟约 多对多 |
| `references/season-1.md` | 赛季机制：模式、认证表、关键目标、兑换、阶段时间线 |
| `references/covenants.md` | 盟约总表 + 各盟约所属干员 |
| `references/operators.md` | 按 Ⅰ–Ⅵ 阶排列的全部干员 |
| `references/synergy.md` | 阵容协同分析（乌萨斯、灵巧、双盟约桥、8 人口骨架） |
| `scripts/query.py` | `op` / `bond` / `tier` / `search` / `sql` 查询 |
| `scripts/gen_references.py` | 从 `data/garrison.db` 重新生成 `references/{covenants,operators}.md` |

## 使用

```bash
python3 scripts/query.py op 奥尔佳
python3 scripts/query.py bond 乌萨斯
python3 scripts/query.py tier 6
python3 scripts/query.py sql "select name,bonds from operators where bond_ids like '%lethaniaShip%'"
```

或直接：

```bash
sqlite3 data/garrison.db
```

作为 Skill 安装（以 omp 为例，其他 Agent 换成对应 skills 目录）：

```bash
ln -s "$PWD" ~/.omp/agent/skills/arknights-garrison-s1-skill
```

## 更新

- 赛季迭代时替换 `data/` 下的 CSV/SQLite（字段结构不变），然后运行 `python3 scripts/gen_references.py`。
- 数据来源与版本记录见 `references/season-1.md` 末尾。

## 许可与声明

- 本仓库代码与整理内容：**GPL-3.0**，见 `LICENSE`。
- 上游解析数据来自 [sganggs/Stronghold-Protocol](https://github.com/sganggs/Stronghold-Protocol)（GPL-3.0），其数据由官方 `activity_table.json` 解析而来。
- 游戏《明日方舟》及其角色、技能、数值等版权归上海鹰角网络科技有限公司（Hypergryph）所有。
- 部分机制描述与官方公告、[PRTS Wiki](https://prts.wiki/) 交叉核对；PRTS 内容采用 CC BY-NC-SA 4.0。
- 本项目为非官方粉丝作品，与鹰角网络无关，不用于商业用途。详见 `NOTICE.md`。
