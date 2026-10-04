"""🧰 第04章の道具箱（さわらなくていいファイル）

モンスターの絵やバーを出したり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは first_monster.py の方だけ。興味があれば読んでもOK！
"""

import os
import sys

USE_COLOR = "NO_COLOR" not in os.environ

# 課題01と同じ「数字の並びで絵を作る」しくみ。
# 0 = なにもない / 1 = 体の色 / 2 = 目 / 3 = ほっぺ / 4 = 白（きば）
FACES = {
    "スライム": [
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 2, 1, 1, 2, 1, 1],
        [1, 1, 2, 1, 1, 2, 1, 1],
        [1, 3, 1, 1, 1, 1, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
    ],
    "ドラゴン": [
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 2, 1, 1, 2, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 4, 1, 1, 4, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
    ],
    "おばけ": [
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 2, 1, 1, 2, 1, 1],
        [1, 1, 2, 1, 1, 2, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 3, 3, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 1, 0, 1],
    ],
}

# 知らない種族の時は、タマゴの絵を出す
EGG = [
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 4, 1, 1, 0],
    [0, 1, 1, 1, 1, 4, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
]

GREY = (160, 160, 160)
FIXED_COLORS = {2: (40, 40, 50), 3: (255, 140, 160), 4: (255, 255, 255)}
PLAIN_TEXT = {0: "  ", 1: "##", 2: "@@", 3: "**", 4: "^^"}


def safe_rgb(color):
    """色が (赤, 緑, 青) の形になっているか調べて、だめなら灰色にする。"""
    if isinstance(color, tuple) and len(color) == 3:
        if all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            return color
    return GREY


def paint(number, body_color):
    """数字1つを、色のついた2文字分の四角にする。"""
    if number == 0 or not USE_COLOR:
        return PLAIN_TEXT.get(number, "  ")
    r, g, b = body_color if number == 1 else FIXED_COLORS[number]
    return f"\033[48;2;{r};{g};{b}m  \033[0m"


def draw_face(kind, color):
    grid = FACES.get(kind, EGG)
    rgb = safe_rgb(color)
    for row in grid:
        print("   " + "".join(paint(number, rgb) for number in row))


def is_blueprint(thing):
    """インスタンスではなく、設計図（クラス）そのものかどうか。"""
    return isinstance(thing, type)


def show_monster(monster):
    """モンスターの顔と情報を表示する。"""
    if monster is None:
        print("🥚 （まだ2匹目がいないよ → TODO 3 で誕生させよう）\n")
        return
    if is_blueprint(monster):
        print("⚠️  Monster の後ろに ( ) がないみたい。")
        print("    それは「設計図そのもの」で、まだ誕生していないよ。\n")
        return

    kind = getattr(monster, "kind", "？？？")
    color = getattr(monster, "color", None)
    draw_face(kind, color)
    if safe_rgb(color) is GREY:
        print("   （色が (赤, 緑, 青) の形になっていないので、灰色にしたよ）")
    if kind not in FACES:
        print("   （知らない種族なので、まだタマゴのまま…）")
    print(f"   なまえ: {getattr(monster, 'name', '？？？')}   種族: {kind}")
    print(f"   HP: {getattr(monster, 'hp', '？？')}   レベル: {getattr(monster, 'level', '？')}\n")


def show_level(monster):
    if monster is None or is_blueprint(monster):
        print("   （2匹目は、まだ誕生していないよ）")
        return
    print(f"   {getattr(monster, 'name', '？？？')} のレベル: {getattr(monster, 'level', '？')}")


def check_todos(blueprint, piko, buddy):
    """TODOができたか、モンスターのふるまいを見て調べる。"""
    print("\n📋 TODOチェック")
    results = []

    test = blueprint("テスト", "ドラゴン", (1, 2, 3))
    kind_ok = getattr(test, "kind", None) == "ドラゴン"
    color_ok = getattr(test, "color", None) == (1, 2, 3)
    ok1 = kind_ok and color_ok
    results.append(ok1)
    if ok1:
        print("  ✅ TODO 1 クリア！ 種族と色を覚えられた")
    elif not hasattr(test, "kind"):
        print("  🔧 TODO 1 まだ: モンスターが kind（種族）を覚えていないみたい")
    elif not hasattr(test, "color"):
        print("  🔧 TODO 1 まだ: モンスターが color（色）を覚えていないみたい")
    elif getattr(test, "kind", None) == (1, 2, 3):
        print("  🔧 TODO 1 まだ: kind と color が入れかわっていないかな？")
    elif not kind_ok:
        print("  🔧 TODO 1 まだ: kind の箱に、受け取った kind 以外が入っているみたい。self.kind = kind かな？")
    else:
        print("  🔧 TODO 1 まだ: color の箱に、受け取った color 以外が入っているみたい。self.color = color かな？")

    ok2 = getattr(test, "hp", None) == 10
    results.append(ok2)
    if ok2:
        print("  ✅ TODO 2 クリア！ 生まれた時の HP が 10 になった")
    else:
        print("  🔧 TODO 2 まだ: 生まれたばかりの子の hp が 10 になっていないよ")

    ok3 = isinstance(buddy, blueprint) and buddy is not piko
    results.append(ok3)
    if ok3:
        print(f"  ✅ TODO 3 クリア！ {buddy.name} が誕生した")
    elif is_blueprint(buddy):
        print("  🔧 TODO 3 まだ: Monster の後ろに ( ) と、名前・種族・色を書こう")
    elif buddy is piko:
        print("  🔧 TODO 3 まだ: それはピコと同じ子だよ。Monster(...) で、もう1匹を誕生させよう")
    else:
        print("  🔧 TODO 3 まだ: 2匹目が誕生していないよ")

    ok4 = getattr(piko, "level", None) == 2 and (not ok3 or buddy.level == 1)
    results.append(ok4)
    if ok4:
        print("  ✅ TODO 4 クリア！ ピコだけレベル2になった")
    else:
        print("  🔧 TODO 4 まだ: ピコのレベルが 2 になっていないよ")

    if all(results):
        print("\n🎉 全部クリア！ 君は、設計図からモンスターを誕生させられるようになった！")
    elif os.environ.get("STRICT_CHECK"):
        sys.exit(1)
