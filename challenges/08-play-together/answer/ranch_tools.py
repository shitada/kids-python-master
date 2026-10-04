"""🧰 第08章の道具箱（さわらなくていいファイル）

モンスターの絵やバーを出したり、対決を進めたり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは play_together.py の方だけ。興味があれば読んでもOK！
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


# ---------- 第08章の道具 ----------

def battle(a, b, rounds=3):
    """a と b の、たいあたり勝負。君が作った tackle を使うよ。"""
    print(f"🏟️  {a.name}（{a.kind}）  VS  {b.name}（{b.kind}）")
    print(f"    {hp_line(a)}")
    print(f"    {hp_line(b)}")
    something_happened = False
    for number in range(1, rounds + 1):
        print(f"\n― ラウンド{number} ―")
        for attacker, target in ((a, b), (b, a)):
            if attacker.hp == 0 or target.hp == 0:
                continue
            power = attacker.power_against(target)
            before = target.hp
            try:
                lost = attacker.tackle(target)
            except Exception as error:  # noqa: BLE001
                print(f"⚠️  tackle でエラーが出たよ → {type(error).__name__}: {error}")
                return None
            if target.hp == before and not lost:
                print(f"💨 {attacker.name} の たいあたり！……でも、何も起きない（TODO 4）")
                continue
            something_happened = True
            note = ""
            if power == 5:
                note = "  こうかは ばつぐんだ！"
            elif power == 2:
                note = "  あまり きいていない……"
            print(f"💥 {attacker.name} の たいあたり！ {target.name} に {lost} ダメージ{note}")
            if isinstance(lost, int) and lost < power:
                print(f"   （{target.name} の HP は {before} しかなかった！）")
            print(f"   {hp_line(target)}")
        if a.hp == 0 or b.hp == 0:
            break
    print()
    if not something_happened:
        print("🤝 勝負はおあずけ（TODO 4 を完成させると、勝負が始まるよ）")
        return None
    if a.hp > b.hp:
        winner = a
    elif b.hp > a.hp:
        winner = b
    else:
        print("🤝 ひきわけ！")
        return None
    print(f"🏅 かちは {winner.name}！")
    return winner


# ---------- ここから下は、答え合わせのしくみ。先に自分で解いてね ----------

def pair(blueprint, hp_a=10, hp_b=10, kind_a="スライム", kind_b="スライム"):
    a = blueprint("テスA", kind_a, (1, 2, 3))
    b = blueprint("テスB", kind_b, (4, 5, 6))
    a.hp, b.hp = hp_a, hp_b
    return a, b


def state(monster):
    return (monster.hp, monster.happy)


def check_todo1(blueprint):
    a, b = pair(blueprint)
    alone, error = try_quietly(lambda: a.can_play_with(a))
    if error is not None:
        return False, f"can_play_with でエラーが出たよ → {type(error).__name__}: {error}"
    twin_a, twin_b = pair(blueprint)
    twin_b.name = twin_a.name
    with_twin, _ = try_quietly(lambda: twin_a.can_play_with(twin_b))
    friend, _ = try_quietly(lambda: a.can_play_with(b))
    if alone is not False:
        return False, "自分自身（同じ本人）とは遊べないよ。self is other なら False を返そう"
    if friend is not True:
        return False, "元気なふたりなら True だよ。is_tired の () を忘れていないかな？（self.is_tired()）"
    if with_twin is not True:
        return False, "同じ名前でも別の子となら遊べるよ。名前ではなく is で「同じ本人？」と聞こう"
    if state(a) != (10, 50):
        return False, "can_play_with は答えるだけのメソッド。ここで遊んだり HP を変えたりしないでね"
    return True, "同じ本人かどうか、見分けられた"


def check_todo2(blueprint):
    cases = [((3, 10), False), ((10, 3), False), ((3, 3), False), ((4, 4), True)]
    for (hp_a, hp_b), expected in cases:
        a, b = pair(blueprint, hp_a, hp_b)
        answer, error = try_quietly(lambda: a.can_play_with(b))
        if error is not None:
            return False, f"can_play_with でエラーが出たよ → {type(error).__name__}: {error}"
        if (a.hp, b.hp) != (hp_a, hp_b):
            return False, "can_play_with は答えるだけのメソッド。ここで HP を変えないでね"
        if answer is not expected:
            if (hp_a, hp_b) == (10, 3):
                return False, "相手（other）がつかれているかも、確かめよう"
            if (hp_a, hp_b) == (3, 10):
                return False, "自分（self）がつかれているかも、確かめよう"
            if (hp_a, hp_b) == (4, 4):
                return False, "ふたりとも元気（HP 4 以上）なら True になるかな？ and と or をまちがえていない？"
            return False, "どちらかがつかれていたら False を返そう"
    return True, "自分と相手、ふたりの元気を確かめられた"


def check_todo3(blueprint):
    a, b = pair(blueprint)
    outsider, _ = pair(blueprint)
    calls_a, calls_b = spy_on(a, "play"), spy_on(b, "play")
    result, error = try_quietly(lambda: a.play_with(b))
    if error is not None:
        return False, f"play_with でエラーが出たよ → {type(error).__name__}: {error}"
    if len(calls_a) == 0 and len(calls_b) == 0:
        if (a.hp, b.hp) != (10, 10):
            return False, "HP を直接変えずに、self.play() と other.play() に頼もう"
        return False, "ふたりとも元気なのに、だれも遊んでいないよ。self.play() と other.play() を呼ぼう"
    if len(calls_b) == 0:
        return False, "自分だけ遊んでいるよ。相手の other.play() にも頼もう"
    if len(calls_a) == 0:
        return False, "相手だけ遊んでいるよ。自分の self.play() も呼ぼう"
    if len(calls_a) != 1 or len(calls_b) != 1:
        return False, "play() は、ふたりとも1回ずつ呼ぼう"
    if result is not True:
        return False, "遊べた時は True を return しよう"
    if state(outsider) != (10, 50):
        return False, "関係ない子まで遊んでいるみたい"
    todo12 = check_todo1(blueprint)[0] and check_todo2(blueprint)[0]
    for hp_a, hp_b, same in ((10, 3, False), (3, 10, False), (10, 10, True)):
        c, d = pair(blueprint, hp_a, hp_b)
        if same:
            d = c
        recorders = [spy_on(c, "play")] if same else [spy_on(c, "play"), spy_on(d, "play")]
        before = (state(c), state(d))
        answer, _ = try_quietly(lambda: c.play_with(d))
        played = sum(len(calls) for calls in recorders)
        if (state(c), state(d)) != before or answer is not False:
            if not todo12:
                return False, "遊ぶところはできた！ あとは TODO 1・2 を完成させると、お休みの判定もできるよ"
            if played:
                return False, "お休みの時は、だれも遊ばないように。can_play_with で確かめるのは、遊ぶ「前」だよ"
            return False, "遊べない時は False を返そう"
    return True, "確かめてから、ふたりにそれぞれ遊んでもらえた"


def check_todo4(blueprint):
    results = []
    for kind_b, hp_b, power in (("ドラゴン", 10, 5), ("スライム", 10, 3), ("ドラゴン", 2, 5)):
        a, b = pair(blueprint, 10, hp_b, "スライム", kind_b)
        calls = spy_on(b, "take_damage")
        lost, error = try_quietly(lambda: a.tackle(b))
        if error is not None:
            return False, f"tackle でエラーが出たよ → {type(error).__name__}: {error}"
        expected_hp = max(0, hp_b - power)
        if a.hp != 10:
            return False, "自分（self）がダメージを受けているよ。相手の other.take_damage に頼もう"
        if b.hp == hp_b and not calls:
            return False, "まだ、相手の HP が減らないよ。other.take_damage(...) を呼ぼう"
        if not calls:
            return False, "相手の HP を直接変えずに、other.take_damage(...) に頼もう"
        if calls != [power]:
            return False, "たいあたりの強さは、self.power_against(other) で決めよう"
        if b.hp != expected_hp:
            return False, "take_damage は1回だけ呼ぼう"
        if lost != hp_b - expected_hp:
            if lost == power:
                return False, "強さではなく、take_damage が返した「本当に減った量」を返そう"
            return False, "take_damage が返した数を、そのまま return しよう"
        results.append(True)
    return True, "相手の take_damage に頼んで、本当に減った量を返せた"


def check_todos(blueprint):
    """TODOができたか、ふるまいを見て調べる。"""
    print("\n📋 TODOチェック")
    checks = [check_todo1(blueprint), check_todo2(blueprint), check_todo3(blueprint), check_todo4(blueprint)]
    results = []
    for number, (ok, message) in enumerate(checks, start=1):
        results.append(ok)
        mark = "✅" if ok else "🔧"
        state_text = "クリア！" if ok else "まだ:"
        print(f"  {mark} TODO {number} {state_text} {message}")
    return report(results, "相手の子を受け取って、相手のメソッドに頼めるようになった！")
