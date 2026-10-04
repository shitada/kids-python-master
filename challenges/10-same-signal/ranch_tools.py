"""🧰 第10章の道具箱（さわらなくていいファイル）

モンスターの絵やバーを出したり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは same_signal.py の方だけ。興味があれば読んでもOK！
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


# ---------- 第10章の道具 ----------

class Balloon:
    """ふうせん。この道具箱の中で作られた、だれも知らない4つめの道具。"""

    def __init__(self):
        self.name = "ふうせん"
        self.icon = "🎈"
        self.times = 0

    def use(self, monster):
        self.times = self.times + 1
        print(f"🎈 {monster.name} は、ふうせんで ぷかぷか！")
        if monster.is_tired():
            monster.sleep()
        else:
            monster.play()
        return True


def new_balloon():
    return Balloon()


def balloon_finale(balloon):
    """ふうせんが使われたかどうかで、最後のひとことを変える。"""
    if balloon.times >= 2:
        print("\n✨ use_all も Trainer も、1行も直していないのに、新しい道具が動いた！")
    else:
        print("\n🎈 ふうせんは、まだだれにも使われていない……（TODO 3・4 を完成させよう）")


def show_team_hp(trainer):
    """チーム全員の HP とごきげんを表示する。"""
    for member in trainer.team:
        print(f"   {hp_line(member)}  ごきげん {member.happy}")


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

class FakeTool:
    """チェック用の、だれも知らない道具。だれに使われたかを記録する。"""

    def __init__(self, answer):
        self.name = "なぞの道具"
        self.icon = "❔"
        self.answer = answer
        self.used_on = []

    def use(self, monster):
        self.used_on.append(monster)
        return self.answer


def test_monster(blueprint, hp=10, name="テスA"):
    monster = blueprint(name, "スライム", (1, 2, 3))
    monster.hp = hp
    return monster


def check_todo1(blueprint, snack_class):
    for amount, hp in ((4, 2), (2, 9)):
        monster = test_monster(blueprint, hp)
        calls = spy_on(monster, "eat")
        snack, error = try_quietly(lambda: snack_class(amount))
        answer, error2 = try_quietly(lambda: snack.use(monster)) if error is None else (None, error)
        error = error or error2
        if error is not None:
            return False, f"Snack でエラーが出たよ → {type(error).__name__}: {error}"
        if not calls:
            if monster.hp != hp:
                return False, "HP を直接ふやさず、monster.eat(...) に頼もう"
            return False, "まだ食べていないよ。monster.eat(self.amount) を呼ぼう"
        if calls != [amount]:
            return False, "食べる量は、おやつが覚えている self.amount にしよう"
        if answer is not True:
            return False, "使えたら True を return しよう"
    return True, "おやつが、use の合図で食べさせられた"


def check_todo2(blueprint, puzzle_class):
    tired = test_monster(blueprint, 3)
    order = spy_order(tired, ["play", "eat"])
    answer, error = try_quietly(lambda: puzzle_class().use(tired))
    if error is not None:
        return False, f"Puzzle でエラーが出たよ → {type(error).__name__}: {error}"
    if order:
        return False, "つかれている子には、何もしないで False を返そう（is_tired で確かめよう）"
    if answer is not False:
        return False, "つかれていて使えなかった時は、False を return しよう"
    fine = test_monster(blueprint, 10)
    order = spy_order(fine, ["play", "eat"])
    answer, _ = try_quietly(lambda: puzzle_class().use(fine))
    if not order:
        return False, "元気な子なら、play() と eat(1) を頼もう"
    if order != [("play", None), ("eat", 1)]:
        return False, "順番は play() → eat(1) だよ。それぞれ1回ずつ"
    if answer is not True:
        return False, "使えたら True を return しよう"
    return True, "パズルも、use の合図で動いた"


def check_todo3(blueprint, use_all):
    monster = test_monster(blueprint)
    tools = [FakeTool(True), FakeTool(False), FakeTool(True)]
    results, error = try_quietly(lambda: use_all(tools, monster))
    if error is not None:
        return False, f"use_all でエラーが出たよ → {type(error).__name__}: {error}"
    used = [len(tool.used_on) for tool in tools]
    if used == [0, 0, 0]:
        return False, "まだ道具を使っていないよ。for で1つずつ tool.use(monster) しよう"
    if used != [1, 1, 1]:
        return False, "道具は全部、1回ずつ使おう"
    if not all(tool.used_on[0] is monster for tool in tools):
        return False, "道具は、受け取った monster に使おう"
    if results is None:
        return False, "答えのリスト results を return しよう"
    if results != [True, False, True]:
        return False, "それぞれの tool.use(monster) の答えを、順番に results に append しよう"
    return True, "知らない道具も、use の合図で全部使えた"


def check_todo4(blueprint, trainer_class):
    mine, _ = try_quietly(lambda: trainer_class("テスA"))
    other, _ = try_quietly(lambda: trainer_class("テスB"))
    a, b, c = test_monster(blueprint, 10, "A"), test_monster(blueprint, 10, "B"), test_monster(blueprint, 10, "C")
    mine.team = [a, b]
    other.team = [c]
    tool = FakeTool(True)
    _, error = try_quietly(lambda: mine.use_on_team(tool))
    if error is not None:
        return False, f"use_on_team でエラーが出たよ → {type(error).__name__}: {error}"
    if not tool.used_on:
        return False, "まだ道具を使っていないよ。チームの1匹ずつに tool.use(member) しよう"
    if any(member is c for member in tool.used_on):
        return False, "よそのチームの子にまで使っているよ。自分のチーム（self.team）だけにしよう"
    if len(tool.used_on) != 2 or tool.used_on[0] is not a or tool.used_on[1] is not b:
        return False, "チームの全員に、1回ずつ使おう"
    return True, "チーム全員に、同じ合図で道具を使えた"


def check_todos(blueprint, snack_class, puzzle_class, use_all, trainer_class):
    """TODOができたか、ふるまいを見て調べる。"""
    checks = [
        check_todo1(blueprint, snack_class),
        check_todo2(blueprint, puzzle_class),
        check_todo3(blueprint, use_all),
        check_todo4(blueprint, trainer_class),
    ]
    return show_report(checks, "種類がちがう道具を、同じ合図で使えるようになった！")
