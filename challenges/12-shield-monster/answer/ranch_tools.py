"""🧰 第12章の道具箱（さわらなくていいファイル）

モンスターの絵やバーを出したり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは shield_monster.py の方だけ。興味があれば読んでもOK！
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


# ---------- 第12章の道具 ----------

def try_demo(action):
    """action を実行する。エラーが出たら、止まらずにエラーの最後の行を見せる。"""
    try:
        action()
    except Exception as error:  # noqa: BLE001
        print(f"   💥 {type(error).__name__}: {error}")


def gauge(monster):
    """バリアの残り回数を [■■] のようなゲージにする。"""
    shield = getattr(monster, "shield", 0)
    if not isinstance(shield, int) or shield < 0:
        return "[？？]"
    full = max(2, shield)
    return "[" + "■" * shield + "□" * (full - shield) + "]"


def show_guard(guard):
    """ガードの顔と、HP・バリアを表示する。"""
    draw_faces([guard])
    if not hasattr(guard, "hp"):
        print("⚠️  ガードは HP を持っていないみたい……（TODO 1）")
    else:
        print(f"   {hp_line(guard)}")
    print(f"   🛡️ バリア {gauge(guard)} 残り {getattr(guard, 'shield', '？')} 回")


def attack_demo(attacker, guard, times=3):
    """attacker が guard に、何回かたいあたりする。"""
    if not hasattr(guard, "hp"):
        print("🥚 ガードが HP を持っていないので、練習試合はおあずけ（TODO 1）")
        return
    for number in range(1, times + 1):
        before_hp = guard.hp
        before_gauge = gauge(guard)
        power = attacker.power_against(guard)
        try:
            lost = attacker.tackle(guard)
        except Exception as error:  # noqa: BLE001
            print(f"⚠️  たいあたりでエラーが出たよ → {type(error).__name__}: {error}")
            return
        print(f"\n― {number}回目 ―  🛡️{before_gauge}")
        if guard.hp == before_hp and not lost:
            print(f"💨 {attacker.name} の たいあたり！……でも、何も起きない（TODO 3・4）")
            continue
        print(f"💥 {attacker.name} の たいあたり！ 強さ {power} → 本当に減ったのは {lost}")
        print(f"   {guard.name} HP {before_hp} → {guard.hp}   🛡️{gauge(guard)}")
        if guard.hp == 0:
            print(f"   （{guard.name} は、もうたおれた！ 0 より下にはならない）")
            break


# ---------- ここから下は、答え合わせのしくみ。先に自分で解いてね ----------

def make_guard(child, name="テスG"):
    guard, error = try_quietly(lambda: child(name, "スライム", (1, 2, 3)))
    return guard, error


def check_todo1(parent, child):
    with spy_on_class(parent, "__init__") as calls:
        guard, error = make_guard(child)
    if error is not None:
        return False, f"ShieldMonster の誕生でエラーが出たよ → {type(error).__name__}: {error}"
    if not calls:
        if hasattr(guard, "hp"):
            return False, "親の __init__ の中身をコピーせずに、super().__init__(name, kind, color) に頼もう"
        return False, "ガードが HP を持っていないよ。super().__init__(name, kind, color) で親に頼もう"
    if len(calls) != 1 or calls[0][0] is not guard:
        return False, "super().__init__(...) は、1回だけ呼ぼう"
    if (guard.name, guard.kind, guard.color) != ("テスG", "スライム", (1, 2, 3)):
        return False, "受け取った name・kind・color を、そのまま親に渡そう"
    if guard.hp != 10:
        return False, "親の準備のあとで、HP を変えていないかな？"
    return True, "親の誕生セット係に、準備をしてもらえた"


def check_todo2(child):
    first, error = make_guard(child, "テスA")
    second, _ = make_guard(child, "テスB")
    if error is not None:
        return False, f"ShieldMonster の誕生でエラーが出たよ → {type(error).__name__}: {error}"
    if "shield" in vars(child):
        return False, "shield は、__init__ の中で self.shield = 2 と作ろう（第09章のクラス属性に注意）"
    if getattr(first, "shield", None) != 2:
        return False, "バリアの残り回数 self.shield を 2 にしよう"
    first.shield = 1
    if second.shield != 2:
        return False, "バリアは、1匹ずつ別々に持とう"
    return True, "ガードだけの属性、バリアを持てた"


def check_todo3(parent, child):
    guard, _ = make_guard(child)
    counts = []
    with spy_on_class(parent, "take_damage") as calls:
        for amount in (5, 0, 5, 5):
            _, error = try_quietly(lambda: guard.take_damage(amount))
            if error is not None:
                return False, f"take_damage でエラーが出たよ → {type(error).__name__}: {error}"
            counts.append(guard.shield)
    if counts[0] == 2:
        return False, "攻撃を受けても、バリアが減っていないよ。self.shield = self.shield - 1"
    if counts[1] != counts[0]:
        return False, "0 のダメージでは、バリアを使わないようにしよう（amount > 0 の時だけ）"
    if counts[3] < 0:
        return False, "バリアがマイナスになったよ。残っている時（self.shield > 0）だけ使おう"
    if counts != [1, 1, 0, 0]:
        return False, "バリアは、攻撃1回につき1つずつ使おう"
    amounts = [amount for _, amount in calls]
    if amounts and amounts != [4, 0, 4, 5]:
        if amounts[0] == 5:
            return False, "バリアを使った時は、amount を 1 へらそう（amount = amount - 1）"
        return False, "へらしたダメージを、親の take_damage に渡そう"
    return True, "バリアで、ダメージを1へらせた"


def check_todo4(parent, child):
    guard, _ = make_guard(child)
    with spy_on_class(parent, "take_damage") as calls:
        lost, error = try_quietly(lambda: guard.take_damage(5))
    if error is not None:
        return False, f"take_damage でエラーが出たよ → {type(error).__name__}: {error}"
    if not calls:
        if guard.hp != 10:
            return False, "HP を自分で計算せずに、super().take_damage(amount) に頼もう"
        return False, "まだ HP が減らないよ。super().take_damage(amount) を呼ぼう"
    if len(calls) != 1 or calls[0][0] is not guard:
        return False, "super().take_damage(amount) は、1回だけ呼ぼう"
    if lost is None:
        return False, "親の答え（本当に減った量）を return しよう"
    weak, _ = make_guard(child)
    weak.shield = 0
    quietly(lambda: weak.take_damage(8))
    last, _ = try_quietly(lambda: weak.take_damage(5))
    if weak.hp != 0 or last != 2:
        return False, "HP が 2 しかない時は、本当に減ったのは 2。親の答えを、そのまま return しよう"
    if lost != 10 - guard.hp:
        return False, "親の take_damage が返した数を、そのまま return しよう"
    return True, "親のルールで HP を減らして、本当に減った量を返せた"


def check_todos(parent, child):
    """TODOができたか、ふるまいを見て調べる。"""
    first = check_todo1(parent, child)
    second = check_todo2(child)
    if first[0]:
        rest = [check_todo3(parent, child), check_todo4(parent, child)]
    else:
        rest = [(False, "先に TODO 1 で、親に誕生の準備をしてもらおう")] * 2
    return show_report([first, second] + rest, "親の仕事を使いながら、自分の仕事を足せるようになった！")
