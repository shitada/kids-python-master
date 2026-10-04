"""🧰 第07章の道具箱（さわらなくていいファイル）

モンスターの絵やバーを出したり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは busy_ranch.py の方だけ。興味があれば読んでもOK！
"""

import random
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


# ---------- 第07章の道具 ----------

EGG_NAMES = ["ナナ", "ポポ", "ゴン", "チビ", "ボブ", "ララ", "テン", "モコ"]
EGG_KINDS = ["スライム", "ドラゴン", "おばけ"]
EGG_COLORS = [(250, 220, 90), (120, 200, 90), (200, 170, 255), (255, 150, 120), (110, 220, 210)]


def deliver_eggs(seed=42):
    """タマゴ便。4個のタマゴ（辞書）のリストを返す。seed を変えると中身が変わるよ。"""
    rng = random.Random(seed)
    eggs = []
    for name in rng.sample(EGG_NAMES, 3):
        eggs.append({"name": name, "kind": rng.choice(EGG_KINDS), "color": rng.choice(EGG_COLORS)})
    # ピコという名前は人気なので、いつも1個は「ピコ」がまざっている
    eggs.insert(1, {"name": "ピコ", "kind": rng.choice(["ドラゴン", "おばけ"]), "color": rng.choice(EGG_COLORS)})
    return eggs


def show_roster(ranch):
    """牧場の名簿を、番号つきで表示する。"""
    print(f"📋 牧場の名簿（{len(ranch)}匹）")
    for index in range(len(ranch)):
        monster = ranch[index]
        earlier = ranch[:index]
        mark = ""
        if any(other is monster for other in earlier):
            mark = "   ← あれ？ この子、さっきもいたよ！"
        elif any(other.name == monster.name for other in earlier):
            mark = "   ← 先輩と同じ名前の、別の子！"
        print(f"   No.{index + 1} {monster}{mark}")


# ---------- ここから下は、答え合わせのしくみ。先に自分で解いてね ----------

def make_test_monsters(blueprint):
    """チェック用のモンスターを作る（同じ名前の別の子もいる）。"""
    a = blueprint("テスA", "スライム", (1, 2, 3))
    b = blueprint("テスB", "ドラゴン", (4, 5, 6))
    c = blueprint("テスC", "おばけ", (7, 8, 9))
    twin = blueprint("テスA", "スライム", (1, 2, 3))
    return a, b, c, twin


def check_todo1(blueprint, hatch_one):
    egg = {"name": "テスト", "kind": "ドラゴン", "color": (1, 2, 3)}
    first, error = try_quietly(lambda: hatch_one(egg))
    second, _ = try_quietly(lambda: hatch_one(egg))
    if error is not None:
        return False, f"hatch_one でエラーが出たよ → {type(error).__name__}: {error}"
    if first is None:
        return False, "まだ何も返していないみたい。return Monster(...) の形かな？"
    if not isinstance(first, blueprint):
        return False, "名前ではなく、Monster(...) で誕生させた「その子」を返そう"
    if (first.name, first.kind, first.color) != ("テスト", "ドラゴン", (1, 2, 3)):
        return False, "名前・種族・色を、egg の中身から入れよう（egg[\"name\"] など）"
    if first is second:
        return False, "2回呼んだら、同じ子が返ってきたよ。呼ばれるたびに Monster(...) で新しく誕生させよう"
    return True, "タマゴから、毎回ちがう子が誕生した"


def check_todo2(blueprint, already_here):
    a, b, c, twin = make_test_monsters(blueprint)
    cases = [
        ([a, b, c], a, True),
        ([a, b, c], b, True),
        ([a, b, c], c, True),
        ([], a, False),
        ([a, b], c, False),
        ([a, b], twin, False),
    ]
    answers = []
    for ranch, monster, expected in cases:
        answer, error = try_quietly(lambda: already_here(ranch, monster))
        if error is not None:
            return False, f"already_here でエラーが出たよ → {type(error).__name__}: {error}"
        answers.append(answer)
    if all(answer is None for answer in answers):
        return False, "まだ何も返していないみたい。True か False を return しよう"
    if answers[5] is True:
        return False, "名前で比べていないかな？ 同じ名前でも別の子だよ。is で「同じ本人？」と聞こう"
    if answers[0] is True and (answers[1] is not True or answers[2] is not True):
        return False, "最初の子がちがっても、まだ次の子がいるよ。return False は for が終わってから"
    if [answer is True for answer in answers] != [expected for _, _, expected in cases]:
        return False, "同じ本人がいたら True、最後まで見つからなければ False になるかな？"
    return True, "同じ本人かどうか、is で見分けられた"


def check_todo3(blueprint, weakest):
    a, b, c, _ = make_test_monsters(blueprint)
    a.hp, b.hp, c.hp = 7, 2, 9
    picked, error = try_quietly(lambda: weakest([a, b, c]))
    if error is not None:
        return False, f"weakest でエラーが出たよ → {type(error).__name__}: {error}"
    if picked is None:
        return False, "まだ何も返していないみたい。いちばん弱い子を return しよう"
    if isinstance(picked, (int, float)):
        return False, "HP の数字ではなく、「その子」を返そう"
    if isinstance(picked, str):
        return False, "名前ではなく、「その子」を返そう"
    if picked is not b:
        return False, "HP がいちばん低い子を返しているかな？（HP 7・2・9 なら、HP 2 の子）"
    a.hp, b.hp, c.hp = 5, 5, 8
    tie, _ = try_quietly(lambda: weakest([a, b, c]))
    if tie is not a:
        return False, "HP が同じ時は、先に名簿にいた子を返そう（< と <= のちがいかな？）"
    empty, error = try_quietly(lambda: weakest([]))
    if error is not None or empty is not None:
        return False, "だれもいない時（空のリスト）は、None を返そう"
    return True, "いちばん弱っている「その子」を見つけられた"


def check_todo4(blueprint, feed_all):
    a, b, c, _ = make_test_monsters(blueprint)
    a.hp, b.hp, c.hp = 2, 9, 10
    calls = [spy_on(monster, "eat") for monster in (a, b, c)]
    outsider = blueprint("ソト", "おばけ", (1, 1, 1))
    outsider.hp = 5
    _, error = try_quietly(lambda: feed_all([a, b, c], 3))
    if error is not None:
        return False, f"feed_all でエラーが出たよ → {type(error).__name__}: {error}"
    if [a.hp, b.hp, c.hp] == [2, 9, 10]:
        return False, "まだ、だれもごはんを食べていないみたい"
    if calls != [[3], [3], [3]]:
        if all(len(call) == 0 for call in calls):
            return False, "HP を直接ふやさず、1匹ずつ eat(amount) に頼もう"
        return False, "全員に1回ずつ、eat(amount) を頼めているかな？（amount の数のまま渡そう）"
    if [a.hp, b.hp, c.hp] != [5, 10, 10] or outsider.hp != 5:
        return False, "HP の増え方がおかしいよ。eat に頼むだけでいいよ"
    return True, "全員に、その子の eat でごはんをあげられた"


def check_todos(blueprint, hatch_one, already_here, weakest, feed_all):
    """TODOができたか、ふるまいを見て調べる。"""
    print("\n📋 TODOチェック")
    checks = [
        check_todo1(blueprint, hatch_one),
        check_todo2(blueprint, already_here),
        check_todo3(blueprint, weakest),
        check_todo4(blueprint, feed_all),
    ]
    results = []
    for number, (ok, message) in enumerate(checks, start=1):
        results.append(ok)
        mark = "✅" if ok else "🔧"
        state = "クリア！" if ok else "まだ:"
        print(f"  {mark} TODO {number} {state} {message}")
    return report(results, "名札と本人を見分けて、「その子」にお世話を頼めるようになった！")
