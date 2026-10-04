"""🧰 第06章の道具箱（さわらなくていいファイル）

モンスターの絵やバーを出したり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは monster_card.py の方だけ。興味があれば読んでもOK！
"""

import contextlib
import io
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


HP_COLOR = (90, 210, 120)
HAPPY_COLOR = (255, 190, 60)
ORIGINAL_ATTRIBUTES = ["name", "kind", "color", "level", "max_hp", "hp", "happy"]


def bar(value, maximum, color):
    """値の大きさを ██████░░░░ のようなバーにする。"""
    if not isinstance(value, (int, float)) or maximum <= 0:
        return "？" * 10
    filled = max(0, min(10, round(value / maximum * 10)))
    blocks = "█" * filled
    if USE_COLOR:
        r, g, b = color
        blocks = f"\033[38;2;{r};{g};{b}m{blocks}\033[0m"
    return blocks + "░" * (10 - filled)


def introduce(monster):
    """print(monster) と同じ。__str__ がまちがっていても、止まらずに教えてくれる。"""
    try:
        print(monster)
    except TypeError as error:
        print(f"⚠️  自己紹介がうまくいかなかったよ → TypeError: {error}")


def try_zukan(print_zukan, ranch):
    """君が作った print_zukan を呼ぶ。__str__ がまちがっていても、止まらずに教えてくれる。"""
    try:
        print_zukan(ranch)
    except TypeError as error:
        print(f"⚠️  図鑑がうまく作れなかったよ → TypeError: {error}")


def title(text):
    print(f"\n===== {text} =====\n")


def show_clues(clues):
    """vars() で取り出した属性を、表にして見せる。"""
    if not clues:
        print("（まだ何も見えない…… TODO 2 で vars(momo) を使ってみよう）")
        return
    print("🔎 モモの中身（属性の名前 : 値）")
    for name, value in clues.items():
        print(f"   {name:<8}: {value!r}")
    print("\n💭 __init__ で用意した属性と、1つずつ見比べてみよう。")


def capture(action):
    """action を実行して、画面に出るはずだった文字を受け取る（チェック用）。"""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        action()
    return buffer.getvalue()


def quiet_str(monster):
    """str(monster) を、画面に何も出さずに作る（チェック用）。"""
    with contextlib.redirect_stdout(io.StringIO()):
        return str(monster)


def check_todos(blueprint, ranch, clues, momo, print_zukan):
    """TODOができたか、モンスターのふるまいを見て調べる。"""
    print("\n📋 TODOチェック")
    results = []

    test = blueprint("テスト", "スライム", (1, 2, 3))
    text = None
    error_text = ""
    if "__str__" in vars(blueprint):
        try:
            text = quiet_str(test)
        except TypeError as error:
            error_text = str(error)
    ok1 = isinstance(text, str) and "テスト" in text and "HP" in text and "10" in text
    results.append(ok1)
    if ok1:
        print("  ✅ TODO 1 クリア！ print で自己紹介できるようになった")
    elif "__str__" not in vars(blueprint):
        near = [name for name in vars(blueprint) if name.strip("_") == "str"]
        if near:
            print(f"  🔧 TODO 1 まだ: {near[0]} があるね。アンダーバー _ は前後2つずつだよ")
        elif "__str__" in vars(sys.modules["__main__"]):
            print("  🔧 TODO 1 まだ: __str__ がクラスの外にあるみたい。ほかのメソッドと字下げをそろえよう")
        else:
            print("  🔧 TODO 1 まだ: __str__ メソッドが見つからないよ")
    elif "positional argument" in error_text:
        print("  🔧 TODO 1 まだ: def __str__(self): のように、( ) の中に self を書こう")
    elif text is None:
        print("  🔧 TODO 1 まだ: __str__ は print ではなく、return で文字（文字列）を返そう")
    elif "{self." in text:
        print("  🔧 TODO 1 まだ: 文字の前に f をつけ忘れているよ → return f\"...\"")
    else:
        print("  🔧 TODO 1 まだ: 自己紹介に、名前と HP（例: HP 10/10）を入れよう")

    ok2 = bool(clues) and clues == vars(momo)
    results.append(ok2)
    if ok2:
        print("  ✅ TODO 2 クリア！ vars でモモの中身をのぞけた")
    else:
        print("  🔧 TODO 2 まだ: clues = vars(momo) にしてみよう")

    capture(test.play)
    extra = [name for name in vars(test) if name not in ORIGINAL_ATTRIBUTES]
    ok3 = test.happy == 60 and not extra
    results.append(ok3)
    if ok3:
        print("  ✅ TODO 3 クリア！ 事件解決！ 遊ぶとごきげんが上がるようになった")
    else:
        print("  🔧 TODO 3 まだ: 遊んでもごきげんが上がらない…… ルーペの結果をよく見よう")

    shown = capture(lambda: try_zukan(print_zukan, ranch))
    ok4 = ok1 and all(quiet_str(monster) in shown for monster in ranch) and "No.3" in shown
    results.append(ok4)
    if ok4:
        print("  ✅ TODO 4 クリア！ 図鑑ができた")
    elif not ok1:
        print("  🔧 TODO 4 まだ: 先に TODO 1 の __str__ を完成させよう")
    elif "No." not in shown:
        print("  🔧 TODO 4 まだ: for の中に、まだ print を書いていないみたい")
    else:
        print("  🔧 TODO 4 まだ: 3匹全員が、番号つきで自己紹介できているかな？")

    if all(results):
        print("\n🎉 全部クリア！ モンスターが自己紹介できて、中身も調べられるようになった！")
    elif os.environ.get("STRICT_CHECK"):
        sys.exit(1)
