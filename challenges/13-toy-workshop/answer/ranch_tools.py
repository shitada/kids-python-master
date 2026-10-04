"""🧰 第13章の道具箱（さわらなくていいファイル）

モンスターの絵やバーを出したり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは my_tool.py の方だけ。興味があれば読んでもOK！
"""

import contextlib
import io
import os
import sys
import traceback
import unicodedata

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


def hp_line(monster):
    """「ピコ HP ███░░ 3/10」のような1行を作る。"""
    hp = getattr(monster, "hp", "？")
    max_hp = getattr(monster, "max_hp", 10)
    return f"{getattr(monster, 'name', '？')} HP {bar(hp, max_hp, HP_COLOR)} {hp}/{max_hp}"


def width(text):
    """ターミナルでの文字のはば（日本語は2マス）。"""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def center(text, size):
    """text を、はば size のまん中に置く。"""
    space = max(0, size - width(text))
    return " " * (space // 2) + text + " " * (space - space // 2)


def draw_faces(monsters, per_row=4):
    """何匹かの顔を、横にならべて表示する。"""
    monsters = list(monsters)
    for start in range(0, len(monsters), per_row):
        group = monsters[start:start + per_row]
        grids = [(FACES.get(getattr(m, "kind", None), EGG), safe_rgb(getattr(m, "color", None))) for m in group]
        for row in range(8):
            print("   " + "  ".join("".join(paint(n, rgb) for n in grid[row]) for grid, rgb in grids))
        print("   " + "  ".join(center(str(getattr(m, "name", "？")), 16) for m in group))
        print()


def title(text):
    print(f"\n===== {text} =====\n")


def quietly(action):
    """action を、画面に何も出さずに実行して、その答えを返す（チェック用）。"""
    with contextlib.redirect_stdout(io.StringIO()):
        return action()


def capture(action):
    """action を実行して、画面に出るはずだった文字を受け取る（チェック用）。"""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        action()
    return buffer.getvalue()


def try_quietly(action):
    """action を静かに実行する。エラーが出たら (None, エラー) を返す（チェック用）。"""
    try:
        return quietly(action), None
    except Exception as error:  # noqa: BLE001  子どものコードのどんなエラーも受け止める
        return None, error


def spy_on(monster, method_name):
    """monster のメソッドが「何回、何を渡されて呼ばれたか」を記録する（チェック用）。"""
    calls = []
    original = getattr(monster, method_name)

    def recorder(*args, **kwargs):
        calls.append(args[0] if args else next(iter(kwargs.values()), None))
        return original(*args, **kwargs)

    setattr(monster, method_name, recorder)
    return calls


@contextlib.contextmanager
def spy_on_class(blueprint, method_name):
    """設計図（クラス）のメソッドが、だれに・何を渡されて呼ばれたかを記録する（チェック用）。
    with の外に出ると、かならず元にもどる。"""
    calls = []
    original = blueprint.__dict__[method_name]

    def recorder(self, *args, **kwargs):
        calls.append((self, args[0] if args else next(iter(kwargs.values()), None)))
        return original(self, *args, **kwargs)

    setattr(blueprint, method_name, recorder)
    try:
        yield calls
    finally:
        setattr(blueprint, method_name, original)


def spy_order(monster, method_names):
    """monster のいくつかのメソッドが、どの順番で呼ばれたかを1つのリストに記録する（チェック用）。"""
    order = []
    for name in method_names:
        original = getattr(monster, name)

        def recorder(*args, _name=name, _original=original, **kwargs):
            order.append((_name, args[0] if args else None))
            return _original(*args, **kwargs)

        setattr(monster, name, recorder)
    return order


def show_report(checks, done_message):
    """TODOチェックの結果を表示して、全部クリアなら True を返す。"""
    print("\n📋 TODOチェック")
    results = []
    for number, (ok, message) in enumerate(checks, start=1):
        results.append(ok)
        mark = "✅" if ok else "🔧"
        state = "クリア！" if ok else "まだ:"
        print(f"  {mark} TODO {number} {state} {message}")
    return report(results, done_message)


def quiet_text(monster):
    """str(monster) を、画面に何も出さずに作る（チェック用）。"""
    with contextlib.redirect_stdout(io.StringIO()):
        return str(monster)


def run_chapter(main, check):
    """main を動かす。とちゅうでエラーが出ても、TODOチェックまで進む。"""
    crashed = False
    try:
        main()
    except Exception as error:  # noqa: BLE001
        crashed = True
        print("\n⚠️  とちゅうでエラーが出て、止まってしまったよ。")
        print("    いちばん下の行を読んでみよう（どの行で起きたかも書いてあるよ）。\n")
        traceback.print_exc(file=sys.stdout)
        print(f"\n    → {type(error).__name__}: {error}")
    ok = check()
    if os.environ.get("STRICT_CHECK") and (crashed or not ok):
        sys.exit(1)


def report(results, done_message):
    """TODOチェックの最後のまとめ。全部クリアなら True を返す。"""
    if all(results):
        print(f"\n🎉 全部クリア！ {done_message}")
        return True
    return False


# ---------- 第13章の道具 ----------

EFFECTS = {"eat": "食べる", "play": "遊ぶ", "sleep": "眠る"}


def show_design(design):
    """設計メモを、カードのように表示する。"""
    effect = design.get("effect")
    print(f"   {design.get('icon', '？')} 名前: {design.get('name', '？')}")
    print(f"   🔢 使える回数: {design.get('max_uses', '？')} 回")
    print(f"   ✨ モンスターに頼む仕事: {effect}（{EFFECTS.get(effect, '？？？ eat・play・sleep から選ぼう')}）")


def try_use(toy, monster, label, check_only=False):
    """道具を1回使って（check_only なら使わずに）、残り回数を表示する。"""
    name = f"{getattr(toy, 'icon', '？')} {label}"
    if not hasattr(toy, "left"):
        print(f"{name}: 残り回数がわからない……（TODO 1）")
        return
    if check_only:
        print(f"{name}: 残り {toy.left} 回")
        return
    before = toy.left
    try:
        answer = toy.use(monster)
    except Exception as error:  # noqa: BLE001
        print(f"⚠️  use でエラーが出たよ → {type(error).__name__}: {error}")
        return
    if answer is True:
        print(f"{name}: 使えた！ 残り {before} → {toy.left} 回\n")
    elif answer is False:
        print(f"{name}: 🛑 もう空っぽ！ 使えなかった（残り {toy.left} 回）\n")
    else:
        print(f"{name}: ❓ {answer!r}（True か False を返そう。TODO 2）\n")


def show_results(tools, results):
    """道具を使った結果（True/False）を、1つずつ表示する。"""
    if not isinstance(results, list) or len(results) != len(tools):
        print("📋 結果がまだ受け取れない……（TODO 3）")
        return
    print("📋 結果")
    for tool, result in zip(tools, results):
        if result is True:
            print(f"   {tool.icon} {tool.name} → ✅ 使えた")
        elif result is False:
            print(f"   {tool.icon} {tool.name} → 🛑 使えなかった")
        else:
            print(f"   {tool.icon} {tool.name} → ❓ {result!r}（True か False を返そう）")


# ---------- ここから下は、答え合わせのしくみ。先に自分で解いてね ----------

def make_toy(toy_class, name, max_uses):
    return try_quietly(lambda: toy_class(name, max_uses))


def check_todo1(toy_class):
    toy, error = make_toy(toy_class, "テスト", 3)
    other, _ = make_toy(toy_class, "ほか", 1)
    if error is not None:
        return False, f"MyToy の誕生でエラーが出たよ → {type(error).__name__}: {error}"
    for attribute in ("name", "max_uses", "left"):
        if not hasattr(toy, attribute):
            return False, f"道具が self.{attribute} を持っていないよ"
    if (toy.name, toy.max_uses) != ("テスト", 3):
        return False, "受け取った name と max_uses を、そのまま覚えよう"
    if "left" in vars(toy_class):
        return False, "残り回数は、道具1つずつが別々に持とう（__init__ の中で self.left）"
    if toy.left != 3 or other.left != 1:
        return False, "はじめの残り回数 self.left は、max_uses と同じにしよう"
    return True, "道具が、自分の名前と残り回数を覚えた"


def check_todo2(toy_class, design, blueprint):
    effect = design.get("effect")
    if effect not in EFFECTS:
        return False, "設計メモの effect は、\"eat\"・\"play\"・\"sleep\" のどれかにしよう"
    toy, error = make_toy(toy_class, "テスト", 2)
    if error is not None or not hasattr(toy, "left"):
        return False, "先に TODO 1 を完成させよう"
    answers, orders, lefts = [], [], []
    for _ in range(3):
        monster = blueprint("テスM", "スライム", (1, 2, 3))
        monster.hp = 5
        order = spy_order(monster, list(EFFECTS))
        answer, error = try_quietly(lambda: toy.use(monster))
        if error is not None:
            return False, f"use でエラーが出たよ → {type(error).__name__}: {error}"
        answers.append(answer)
        orders.append([name for name, _ in order])
        lefts.append(toy.left)
    if orders[0] == []:
        return False, f"まだモンスターに何も頼んでいないよ。設計メモの effect は {effect} → monster.{effect}(...) を呼ぼう"
    if orders[0] != [effect]:
        return False, f"設計メモの effect は {effect} なのに、{', '.join(orders[0])} を頼んでいるよ。どちらかをそろえよう"
    if lefts[0] != 1:
        return False, "使ったら、残り回数を 1 へらそう（self.left = self.left - 1）"
    if lefts[2] < 0:
        return False, "残り回数がマイナスになったよ。0 の時は使わずに False を返そう"
    if orders[2] != []:
        return False, "残り回数が 0 の時は、モンスターに何も頼まずに False を返そう"
    if answers != [True, True, False]:
        return False, "使えた時は True、空っぽで使えなかった時は False を return しよう"
    return True, "設計メモどおりに働いて、回数も数えられた"


def check_todo3(toy_class):
    for max_uses in (1, 3):
        toy, error = make_toy(toy_class, "テスト", max_uses)
        if error is not None or not hasattr(toy, "left"):
            return False, "先に TODO 1 を完成させよう"
        toy.left = 0
        _, error = try_quietly(toy.refill)
        if error is not None:
            return False, f"refill でエラーが出たよ → {type(error).__name__}: {error}"
        if toy.left == 0:
            return False, "まだ補充されていないよ。self.left を満タン（self.max_uses）にもどそう"
        if toy.left != max_uses:
            return False, "補充したら、残り回数は self.max_uses と同じになるかな？"
    return True, "道具を、満タンに補充できた"


def check_todo4(calc_fee, blueprint):
    if isinstance(calc_fee, type):
        return False, "入場料の計算は、覚えておくことがないので、クラスではなく関数（def calc_fee）にしよう"
    for hp, expected in ((10, 50), (4, 50), (3, 25), (0, 25)):
        monster = blueprint("テスM", "スライム", (1, 2, 3))
        monster.hp = hp
        before = (monster.hp, monster.happy)
        fee, error = try_quietly(lambda: calc_fee(monster))
        if error is not None:
            return False, f"calc_fee でエラーが出たよ → {type(error).__name__}: {error}"
        if (monster.hp, monster.happy) != before:
            return False, "入場料を計算するだけで、モンスターの HP などは変えないでね"
        if fee is None:
            return False, "入場料を return しよう"
        if fee != expected:
            return False, "つかれている子（is_tired() が True）は 25円、それ以外は 50円 になるかな？"
    return True, "覚えることのない計算は、ふつうの関数で書けた"


def check_todos(toy_class, calc_fee, design, blueprint):
    """TODOができたか、ふるまいを見て調べる。"""
    checks = [
        check_todo1(toy_class),
        check_todo2(toy_class, design, blueprint),
        check_todo3(toy_class),
        check_todo4(calc_fee, blueprint),
    ]
    return show_report(checks, "自分で設計した道具が、牧場で動くようになった！")
