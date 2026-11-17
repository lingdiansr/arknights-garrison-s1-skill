#!/usr/bin/env python3
"""Query the local 卫戍协议·规程·序列Ⅰ dataset (garrison.db).

Examples:
  python3 query.py op 霍尔海雅
  python3 query.py bond 奥术
  python3 query.py tier 6
  python3 query.py search 术师
  python3 query.py sql "select name,bonds from operators where tier=6"
"""
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "garrison.db"


def rows(sql, args=()):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in con.execute(sql, args)]
    finally:
        con.close()


def show_op(name):
    ops = rows("SELECT * FROM operators WHERE name = ? OR appellation = ?",
               (name, name))
    if not ops:
        ops = rows("SELECT * FROM operators WHERE name LIKE ?", (f"%{name}%",))
    for o in ops:
        print(f"{o['tier']}阶 {o['name']} ({o['appellation']}) "
              f"{o['rarity']}★ {o['profession']}/{o['sub_profession']} "
              f"价格{o['price']} 类型={o['chess_type']}")
        print(f"  盟约: {o['bonds'] or '-'}")
        print(f"  特质({o['ability_type']}):")
        print(f"    基础: {o['ability_base']}")
        print(f"    精锐: {o['ability_elite']}")
        print(f"  基础状态: {o['base_status']}")
        print(f"  精锐状态: {o['elite_status']}")
        if o["prototype_char_id"]:
            print(f"  原型: {o['prototype_name'] or '-'} ({o['prototype_char_id']})")
        print()


def show_bond(name):
    bs = rows("SELECT * FROM bonds WHERE name = ? OR bond_id = ?", (name, name))
    if not bs:
        bs = rows("SELECT * FROM bonds WHERE name LIKE ?", (f"%{name}%",))
    for b in bs:
        print(f"【{b['name']}】 {'核心盟约' if b['is_core'] else '附加盟约'} "
              f"激活{b['active_count']}人 阈值{b['thresholds']} "
              f"叠层模式={b['count_mode']}")
        print(f"  {b['desc']}")
        ops = rows("SELECT tier,name FROM operator_bonds WHERE bond=? "
                   "ORDER BY tier,name", (b["name"],))
        print("  所属干员: " + ("、".join(f"{o['tier']}阶{o['name']}" for o in ops)
                              if ops else "-"))
        print()


def show_tier(t):
    ops = rows("SELECT tier,name,rarity,profession,bonds FROM operators "
               "WHERE tier=? ORDER BY name", (int(t),))
    for o in ops:
        print(f"{o['tier']}阶 {str(o['name']):<10} {o['rarity']}★ "
              f"{str(o['profession'] or '-'):<8} {o['bonds'] or '-'}")
    print(f"\n共 {len(ops)} 名")


def search(kw):
    like = f"%{kw}%"
    ops = rows("SELECT tier,name,rarity,profession,bonds,ability_base "
               "FROM operators WHERE name LIKE ? OR appellation LIKE ? "
               "OR bonds LIKE ? OR ability_base LIKE ? ORDER BY tier,name",
               (like, like, like, like))
    for o in ops:
        print(f"{o['tier']}阶 {str(o['name']):<10} {o['rarity']}★ "
              f"{str(o['profession'] or '-'):<8} {o['bonds'] or '-'}")
    print(f"\n共 {len(ops)} 条")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "op" and rest:
        show_op(" ".join(rest))
    elif cmd == "bond" and rest:
        show_bond(" ".join(rest))
    elif cmd == "tier" and rest:
        show_tier(rest[0])
    elif cmd == "search" and rest:
        search(" ".join(rest))
    elif cmd == "sql" and rest:
        for r in rows(" ".join(rest)):
            print(" | ".join(f"{k}={v}" for k, v in r.items()))
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
