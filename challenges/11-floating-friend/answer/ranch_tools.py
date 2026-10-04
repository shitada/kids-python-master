"""🧰 第11章の道具箱（さわらなくていいファイル）

モンスターの絵やバーを出したり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは floating_monster.py の方だけ。興味があれば読んでもOK！
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


# ---------- 第11章の道具 ----------

def show_team_hp(trainer):
    """チーム全員の HP とごきげんを表示する。"""
    for member in trainer.team:
        print(f"   {hp_line(member)}  ごきげん {member.happy}")


def try_hatch(hatch):
    """hatch() を呼んで、誕生した子を返す。うまくいかない時は、理由を教えて None を返す。"""
    try:
        baby = hatch()
    except TypeError as error:
        print(f"⚠️  フワが誕生できなかったよ → TypeError: {error}")
        print("    （TODO 1 で、Monster を受けついでいるかな？）")
        return None
    if baby is None:
        print("🥚 フワのタマゴは、まだ割れない……（TODO 2）")
    return baby


# ---------- ここから下は、答え合わせのしくみ。先に自分で解いてね ----------

def make_floating(child):
    monster, error = try_quietly(lambda: child("テスF", "おばけ", (1, 2, 3)))
    return monster, error


def check_todo1(parent, child):
    if child is parent:
        return False, "FloatingMonster は、Monster とは別の設計図にしよう"
    if not issubclass(child, parent):
        return False, "class FloatingMonster(Monster): のように、カッコの中に親（Monster）を書こう"
    return True, "FloatingMonster は、Monster を受けついだ"


def check_todo2(parent, child, hatch_fuwa):
    fuwa, error = try_quietly(hatch_fuwa)
    if error is not None:
        return False, f"hatch_fuwa でエラーが出たよ → {type(error).__name__}: {error}"
    if fuwa is None:
        return False, "まだ何も返していないみたい。return FloatingMonster(...) しよう"
    if type(fuwa) is parent:
        return False, "Monster(...) ではなく、FloatingMonster(...) で誕生させよう"
    if not isinstance(fuwa, child):
        return False, "FloatingMonster(...) で誕生させた子を返そう"
    if (getattr(fuwa, "name", None), getattr(fuwa, "kind", None)) != ("フワ", "おばけ"):
        return False, "名前は \"フワ\"、種族は \"おばけ\" にしよう"
    if getattr(fuwa, "hp", None) != 10:
        return False, "フワの HP が 10 になっていないよ。__init__ は書かずに、親のものを使おう"
    return True, "親の誕生セット係（__init__）で、フワが誕生した"


def check_todo3(parent, child):
    if "play" not in vars(child):
        return False, "FloatingMonster の中に、def play(self): を書こう（親と同じ名前で）"
    cases = [((6, 50), (5, 60)), ((6, 95), (5, 100)), ((0, 50), (0, 60))]
    for (hp, happy), expected in cases:
        fuwa, error = make_floating(child)
        if error is not None:
            return False, f"フワの誕生でエラーが出たよ → {type(error).__name__}: {error}"
        fuwa.hp, fuwa.happy = hp, happy
        _, error = try_quietly(fuwa.play)
        if error is not None:
            return False, f"play でエラーが出たよ → {type(error).__name__}: {error}"
        got = (fuwa.hp, fuwa.happy)
        if got != expected:
            if got[0] == hp - 3 or got[0] == max(0, hp - 3):
                return False, "HP が 3 減っているよ。フワは 1 だけ減らそう"
            if got[0] < 0:
                return False, "HP がマイナスになったよ。0 より小さくしないルールも書こう"
            if got[1] > 100:
                return False, "ごきげんが 100 をこえたよ。100 で止めよう"
            if got[1] == happy:
                return False, "ごきげんも 10 増やそう"
            return False, "ごきげんは +10（100 まで）、HP は −1（0 まで）になるかな？"
    normal = parent("テスN", "スライム", (1, 2, 3))
    normal.hp = 6
    quietly(normal.play)
    if normal.hp != 3:
        return False, "ふつうの Monster の play まで変わっているよ。Monster（monster.py）は直さないでね"
    return True, "フワだけ、遊び方が変わった（オーバーライド）"


def check_todo4(parent, child):
    if "is_tired" not in vars(child):
        return False, "FloatingMonster の中に、def is_tired(self): を書こう"
    for hp, expected in ((1, True), (0, True), (2, False), (10, False)):
        fuwa, _ = make_floating(child)
        fuwa.hp = hp
        answer, error = try_quietly(fuwa.is_tired)
        if error is not None:
            return False, f"is_tired でエラーが出たよ → {type(error).__name__}: {error}"
        if answer is None:
            return False, "答えを return しよう（return self.hp <= 1）"
        if answer is not expected:
            return False, "HP が 1 以下なら True、2 以上なら False になるかな？"
    normal = parent("テスN", "スライム", (1, 2, 3))
    normal.hp = 3
    if quietly(normal.is_tired) is not True:
        return False, "ふつうの Monster の is_tired まで変わっているよ"
    return True, "フワだけ、つかれにくくなった"


def check_todos(parent, child, hatch_fuwa):
    """TODOができたか、ふるまいを見て調べる。"""
    first = check_todo1(parent, child)
    checks = [first]
    if first[0]:
        checks += [check_todo2(parent, child, hatch_fuwa), check_todo3(parent, child), check_todo4(parent, child)]
    else:
        checks += [(False, "先に TODO 1 で、Monster を受けつごう")] * 3
    return show_report(checks, "設計図を受けついで、一部だけ書きかえられるようになった！")
