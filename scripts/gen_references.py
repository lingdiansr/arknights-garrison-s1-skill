#!/usr/bin/env python3
"""Regenerate references/covenants.md and references/operators.md from data/garrison.db.

Run from the skill root: python3 scripts/gen_references.py
"""
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "garrison.db"
OUT = ROOT / "references"

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row


def q(sql, *args):
    return [dict(r) for r in con.execute(sql, args)]


def esc(s):
    return (s or "").replace("\n", "；").replace("|", "\\|")


def covenants():
    lines = [
        "# 盟约总表（卫戍协议·规程·序列Ⅰ）", "",
        "数据版本 `act3autochess-v3_1`。核心盟约 3 人激活、阈值 3/6；附加盟约多数 2 人。", "",
    ]
    bonds = q("select * from bonds order by is_core desc, bond_order")
    for title, core in (("核心盟约", 1), ("附加盟约", 0)):
        lines += [f"## {title}", "", "| 盟约 | 激活 | 阈值 | 效果 |", "|---|---|---|---|"]
        for b in bonds:
            if bool(b["is_core"]) == bool(core):
                lines.append(
                    f"| {b['name']} | {b['active_count']} | {b['thresholds']} | {esc(b['desc'])} |")
        lines.append("")
    lines += ["## 各盟约所属干员", ""]
    for b in bonds:
        ops = q("select tier,name from operator_bonds where bond=? order by tier", b["name"])
        roster = "、".join(f"{o['tier']}阶{o['name']}" for o in ops)
        lines.append(f"- **{b['name']}**（{len(ops)}）：{roster}")
    return "\n".join(lines) + "\n"


def operators():
    ops = q("select * from operators order by tier, name")
    lines = [
        "# 干员总表（卫戍协议·规程·序列Ⅰ）", "",
        f"共 {len(ops)} 名（含 2 名隐藏、14 名 visible=false）。等阶 = Ⅰ~Ⅵ。", "",
    ]
    cur = None
    for o in ops:
        if o["tier"] != cur:
            cur = o["tier"]
            lines += [f"## {cur} 阶", "",
                      "| 干员 | 星级 | 职业/分支 | 盟约 | 卫戍能力 | 技能 |",
                      "|---|---|---|---|---|---|"]
        lines.append(
            f"| {o['name']} | {o['rarity']}★ | {o['profession']}/{o['sub_profession'] or '-'} "
            f"| {o['bonds'] or '-'} | {o['ability_type']}：{esc(o['ability_base'])}"
            f"<br>精锐：{esc(o['ability_elite'])} | {o['default_skill'] or '-'} |")
    return "\n".join(lines) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "covenants.md").write_text(covenants(), encoding="utf-8")
    (OUT / "operators.md").write_text(operators(), encoding="utf-8")
    print("regenerated references/covenants.md and references/operators.md")


if __name__ == "__main__":
    main()
