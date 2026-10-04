"""🧰 第09章の道具箱（さわらなくていいファイル）

チームを表示したり、交流戦を進めたり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは trainer_team.py の方だけ。興味があれば読んでもOK！
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


# ---------- 第09章の道具 ----------

def names(team):
    """チームの子の名前を「ピコ・ガブ」のようにつなげる。"""
    if not team:
        return "（だれもいない）"
    return "・".join(member.name for member in team)


def team_of(trainer):
    """トレーナーのチーム表。まだなければ空のリストとして扱う。"""
    team = getattr(trainer, "team", None)
    return team if isinstance(team, list) else []


def show_slots(trainer):
    """「🎒 ミナ [ピコ][ガブ][空き]」のように、チームの枠を表示する。"""
    team = team_of(trainer)
    slots = [f"[{member.name}]" for member in team]
    slots += ["[空き]"] * max(0, getattr(trainer, "max_team", 3) - len(team))
    print(f"🎒 {trainer.name:<4} " + "".join(slots))


def show_hp(trainer):
    """チーム全員の HP を表示する。"""
    print(f"🎒 {trainer.name} のチーム")
    for member in team_of(trainer):
        print(f"   {hp_line(member)}")
    if not team_of(trainer):
        print("   （だれもいない）")


def first_match(a, b):
    """a と b のチームの先鋒（1番目の子）どうしで、ふたり遊びをする。"""
    team_a, team_b = team_of(a), team_of(b)
    if not team_a or not team_b:
        print("🥚 先鋒がそろっていないので、交流戦はおあずけ")
        return
    first_a, first_b = team_a[0], team_b[0]
    print(f"{a.name} の先鋒 {first_a.name}  ↔  {b.name} の先鋒 {first_b.name}")
    draw_faces([first_a, first_b])
    if first_a.play_with(first_b):
        print("🏅 こうりゅうメダル！ ふたりとも、なかよくなった！")
    else:
        print("🛑 今回はお休み。また今度遊ぼうね")


# ---------- ここから下は、答え合わせのしくみ。先に自分で解いてね ----------

def make_trainers(blueprint):
    first, error = try_quietly(lambda: blueprint("テスA"))
    second, _ = try_quietly(lambda: blueprint("テスB"))
    return first, second, error


def check_todo1(blueprint):
    first, second, error = make_trainers(blueprint)
    if error is not None:
        return False, f"Trainer の誕生でエラーが出たよ → {type(error).__name__}: {error}"
    if not hasattr(first, "team"):
        return False, "トレーナーが team を持っていないよ。self. を忘れていないかな？"
    if not isinstance(first.team, list):
        return False, "self.team に、空っぽのリスト [] を用意しよう"
    if first.team is second.team or "team" in vars(blueprint):
        return False, "チーム表が、トレーナーみんなで1つになっているよ。__init__ の中で self.team = [] と作ろう"
    if first.team != []:
        return False, "誕生した時のチーム表は、空っぽ [] にしよう"
    return True, "トレーナーごとに、自分だけのチーム表ができた"


def check_todo2(blueprint, monster_blueprint):
    trainer, _, _ = make_trainers(blueprint)
    a = monster_blueprint("テスA", "スライム", (1, 2, 3))
    b = monster_blueprint("テスB", "ドラゴン", (4, 5, 6))
    c = monster_blueprint("テスC", "おばけ", (7, 8, 9))
    twin = monster_blueprint("テスA", "スライム", (1, 2, 3))
    answers = []
    for monster in (a, a, twin, b, c):
        answer, error = try_quietly(lambda: trainer.recruit(monster))
        if error is not None:
            return False, f"recruit でエラーが出たよ → {type(error).__name__}: {error}"
        answers.append(answer)
    team = team_of(trainer)
    if any(answer is None for answer in answers):
        return False, "入れたら True、入れなかったら False を return しよう（return を忘れていないかな？）"
    if not team:
        return False, "チームに、だれも入っていないよ。self.team.append(monster) しよう"
    if any(isinstance(member, str) for member in team):
        return False, "名前ではなく、モンスター本人を append しよう"
    if answers[1] is not False or team.count(a) > 1:
        return False, "同じ本人は、2回入れないよ。already_here(self.team, monster) で確かめよう"
    if answers[2] is not True:
        return False, "同じ名前でも、別の子は入れるよ。名前ではなく本人（is）で比べよう"
    if answers[4] is not False or len(team) > 3:
        return False, "チームは3匹まで。len(self.team) >= self.max_team なら False を返そう"
    if answers != [True, False, True, True, False] or team[0] is not a:
        return False, "入れた時は True、入れなかった時は False になるかな？"
    return True, "同じ本人と、4匹目を断って、チームを作れた"


def check_todo3(blueprint, monster_blueprint):
    mine, other, _ = make_trainers(blueprint)
    a = monster_blueprint("テスA", "スライム", (1, 2, 3))
    b = monster_blueprint("テスB", "ドラゴン", (4, 5, 6))
    c = monster_blueprint("テスC", "おばけ", (7, 8, 9))
    a.hp, b.hp, c.hp = 2, 9, 5
    mine.team = [a, b]
    other.team = [c]
    calls = [spy_on(monster, "eat") for monster in (a, b, c)]
    _, error = try_quietly(lambda: mine.care_all(3))
    if error is not None:
        return False, f"care_all でエラーが出たよ → {type(error).__name__}: {error}"
    if (a.hp, b.hp) == (2, 9):
        return False, "まだ、チームのだれもごはんを食べていないよ"
    if calls[2] or c.hp != 5:
        return False, "よそのチームの子まで食べているよ。自分のチーム（self.team）だけにしよう"
    if calls[0] != [3] or calls[1] != [3]:
        if not calls[0] and not calls[1]:
            return False, "HP を直接ふやさず、1匹ずつ eat(amount) に頼もう"
        return False, "チームの全員に1回ずつ、eat(amount) を頼めているかな？"
    if (a.hp, b.hp) != (5, 10):
        return False, "HP の増え方がおかしいよ。eat に頼むだけでいいよ"
    return True, "号令ひとつで、自分のチームだけをお世話できた"


def check_todo4(blueprint, monster_blueprint):
    trainer, empty, _ = make_trainers(blueprint)
    a = monster_blueprint("テスA", "スライム", (1, 2, 3))
    b = monster_blueprint("テスB", "ドラゴン", (4, 5, 6))
    trainer.team = [a, b]
    empty.team = []
    try:
        shown = capture(trainer.show_team)
        shown_empty = capture(empty.show_team)
    except Exception as error:  # noqa: BLE001
        return False, f"show_team でエラーが出たよ → {type(error).__name__}: {error}"
    if quiet_text(a) not in shown and quiet_text(b) not in shown:
        if a.name in shown or b.name in shown:
            return False, "名前だけでなく、{member} と書いて自己紹介まるごとを出そう（__str__ が使われるよ）"
        return False, "チームの子を、for で1匹ずつ自己紹介（print）しよう"
    if quiet_text(a) not in shown or quiet_text(b) not in shown:
        return False, "チームの全員を紹介できているかな？"
    if "1" not in shown or "2" not in shown:
        return False, "番号もつけよう（1. 2. ……）"
    if "まだ" not in shown_empty:
        return False, "だれもいない時は「（まだ仲間がいない）」と表示しよう"
    if "まだ" in shown:
        return False, "仲間がいる時は「まだ仲間がいない」と出さないようにしよう"
    return True, "チームのみんなを紹介できた"


def quiet_text(monster):
    with contextlib.redirect_stdout(io.StringIO()):
        return str(monster)


def check_todos(blueprint, monster_blueprint):
    """TODOができたか、ふるまいを見て調べる。"""
    print("\n📋 TODOチェック")
    first = check_todo1(blueprint)
    checks = [first]
    for check in (check_todo2, check_todo3, check_todo4):
        if first[0]:
            checks.append(check(blueprint, monster_blueprint))
        else:
            checks.append((False, "先に TODO 1 のチーム表を用意しよう"))
    results = []
    for number, (ok, message) in enumerate(checks, start=1):
        results.append(ok)
        mark = "✅" if ok else "🔧"
        state_text = "クリア！" if ok else "まだ:"
        print(f"  {mark} TODO {number} {state_text} {message}")
    return report(results, "トレーナーがチームを持って、みんなにお世話を頼めるようになった！")
