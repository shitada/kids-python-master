"""🧰 第14章の道具箱（さわらなくていいファイル）

モンスターの絵やバーを出したり、TODOチェックをしたりする道具が入っているよ。
今回の勉強に必要なのは ranch_day.py の方だけ。興味があれば読んでもOK！
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


# ---------- 第14章の道具 ----------

from pathlib import Path

ROMAJI = {"ピコ": "PIKO", "フワ": "FUWA", "ガード": "GUARD", "モモ": "MOMO", "ガブ": "GABU",
          "ナナ": "NANA", "ポポ": "POPO", "ガブリン": "GABURIN"}
OUTPUT = Path(__file__).parent / "output"
LAST_CALLS = []


def show_teams(trainers):
    """トレーナーのチームを、顔つきで表示する。"""
    for trainer in trainers:
        team = getattr(trainer, "team", [])
        print(f"🎒 {trainer.name} のチーム")
        if not team:
            print("   （まだだれもいない……TODO 1）\n")
            continue
        draw_faces(team)


def take_record(monsters):
    """その時のようすを、数字や文字を「写して」記録する（本人の名札は入れない）。"""
    record = []
    for monster in monsters:
        record.append({
            "name": monster.name, "kind": monster.kind, "color": monster.color,
            "hp": monster.hp, "max_hp": monster.max_hp, "happy": monster.happy,
        })
    print(f"📝 {len(record)}匹のようすを、記録帳に書き写したよ")
    return record


def print_newspaper(morning, evening, mvp):
    """新聞の中身を、ターミナルに表示する。"""
    print("📰 ランチ・タイムズ（牧場新聞）")
    if not morning:
        print("   （記事にする仲間が、まだいない……）")
    for before, after in zip(morning, evening):
        name = after["name"] + " " * max(0, 6 - width(after["name"]))
        print(f"   {name} HP {before['hp']:>2} → {after['hp']:>2}   "
              f"ごきげん {before['happy']:>3} → {after['happy']:>3}")
    if mvp is None:
        print("🏅 今日のMVP: ？？？" + ("（仲間がいないよ）" if not morning else "（TODO 3）"))
    else:
        print(f"🏅 今日のMVP: {mvp.name}（ごきげん {mvp.happy}）")


def latin(name, number):
    return ROMAJI.get(name, f"No.{number}")


def save_newspaper(morning, evening, mvp):
    """朝と夕方の記録と MVP から、新聞の画像（PNG）を作って、その場所を返す。"""
    LAST_CALLS.append((morning, evening, mvp))
    from PIL import Image, ImageDraw, ImageFont

    cell = 5
    row_height = 8 * cell + 14
    width = 520
    height = 80 + row_height * max(1, len(evening)) + 40
    image = Image.new("RGB", (width, height), (250, 246, 232))
    draw = ImageDraw.Draw(image)
    try:
        big, font = ImageFont.load_default(size=22), ImageFont.load_default(size=13)
    except TypeError:  # 古い Pillow
        big = font = ImageFont.load_default()
    draw.rectangle([0, 0, width, 54], fill=(40, 40, 60))
    draw.text((16, 6), "THE RANCH TIMES", fill=(255, 230, 120), font=big)
    draw.text((16, 34), "MORNING -> EVENING   HP / HAPPY", fill=(220, 220, 240), font=font)
    top = 70
    for number, (before, after) in enumerate(zip(morning, evening), start=1):
        grid = FACES.get(after["kind"], EGG)
        rgb = safe_rgb(after["color"])
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value == 0:
                    continue
                color = rgb if value == 1 else FIXED_COLORS[value]
                left = 16 + x * cell
                upper = top + y * cell
                draw.rectangle([left, upper, left + cell - 1, upper + cell - 1], fill=color)
        name = latin(after["name"], number)
        star = "  * MVP *" if mvp is not None and after["name"] == mvp.name and after["happy"] == mvp.happy else ""
        draw.text((80, top + 4), f"{name}{star}", fill=(40, 40, 60), font=font)
        draw.text((80, top + 20), f"HP {before['hp']} -> {after['hp']}   HAPPY {before['happy']} -> {after['happy']}",
                  fill=(80, 80, 100), font=font)
        top += row_height
    winner = latin(mvp.name, 0) if mvp is not None else "???"
    draw.text((16, height - 32), f"TODAY'S MVP: {winner}", fill=(200, 60, 80), font=big)
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / "ranch_times.png"
    image.save(path)
    return str(path.relative_to(Path.cwd())) if path.is_relative_to(Path.cwd()) else str(path)


# ---------- ここから下は、答え合わせのしくみ。先に自分で解いてね ----------

def cast(blueprint):
    return [blueprint(name, "スライム", (1, 2, 3)) for name in ("テスA", "テスB", "テスC", "テスD", "テスE")]


def check_todo1(blueprint, trainer_class, prepare_teams):
    mina, ryo = trainer_class("テスミ"), trainer_class("テスリ")
    a, b, c, d, e = cast(blueprint)
    calls_mina, calls_ryo = spy_on(mina, "recruit"), spy_on(ryo, "recruit")
    _, error = try_quietly(lambda: prepare_teams(mina, ryo, a, b, c, d, e))
    if error is not None:
        return False, f"prepare_teams でエラーが出たよ → {type(error).__name__}: {error}"
    if not mina.team and not ryo.team:
        return False, "まだ、だれもチームに入っていないよ。mina.recruit(piko) のように頼もう"
    if not calls_mina or not calls_ryo:
        return False, "チームに直接 append せず、トレーナーの recruit に頼もう"
    if len(mina.team) != 3 or len(ryo.team) != 2:
        return False, "ミナは3匹（ピコ・フワ・ガード）、リョウは2匹（モモ・ガブ）だよ"
    if not (mina.team[0] is a and mina.team[1] is b and mina.team[2] is c and ryo.team[0] is d and ryo.team[1] is e):
        return False, "チームに入れる子と順番を、もう一度確かめよう（ミナ: ピコ→フワ→ガード、リョウ: モモ→ガブ）"
    return True, "2つのチームができた"


def check_todo2(blueprint, trainer_class, run_morning):
    trainer = trainer_class("テスミ")
    trainer.team = cast(blueprint)[:2]
    order = spy_order(trainer, ["care_all", "use_on_team"])
    toy = object()
    _, error = try_quietly(lambda: run_morning(trainer, toy))
    if error is not None and order[-1:] != [("use_on_team", toy)]:
        return False, f"run_morning でエラーが出たよ → {type(error).__name__}: {error}"
    names = [name for name, _ in order]
    if not names:
        return False, "まだ号令をかけていないよ。trainer.care_all(2) と trainer.use_on_team(toy) を呼ぼう"
    if names[0] != "care_all" and "care_all" in names or names == ["use_on_team"]:
        return False, "順番は care_all(2) → use_on_team(toy)。先に care_all(2) をしよう"
    if "care_all" not in names:
        return False, "trainer.care_all(2) で、全員にごはんをあげよう"
    if "use_on_team" not in names:
        return False, "trainer.use_on_team(toy) で、全員に道具を使おう"
    if order != [("care_all", 2), ("use_on_team", toy)]:
        return False, "順番は care_all(2) → use_on_team(toy)。それぞれ1回ずつ、受け取った toy を渡そう"
    return True, "トレーナーに、朝の号令をかけてもらえた"


def check_todo3(blueprint, choose_mvp):
    a, b, c, d, _ = cast(blueprint)
    a.happy, b.happy, c.happy, d.happy = 60, 80, 80, 50
    picked, error = try_quietly(lambda: choose_mvp([a, b, c, d]))
    if error is not None:
        return False, f"choose_mvp でエラーが出たよ → {type(error).__name__}: {error}"
    if picked is None:
        return False, "まだ何も返していないみたい。いちばんごきげんな子を return しよう"
    if isinstance(picked, (int, str)):
        return False, "数字や名前ではなく、「その子」本人を返そう"
    if picked is c:
        return False, "ごきげんが同じ時は、先にいた子を返そう（> と >= のちがいかな？）"
    if picked is not b:
        return False, "いちばんごきげん（happy が大きい）子を返そう"
    empty, error = try_quietly(lambda: choose_mvp([]))
    if error is not None or empty is not None:
        return False, "だれもいない時（空のリスト）は、None を返そう"
    return True, "今日のMVP（本人）を選べた"


def check_todo4(blueprint, publish):
    a, _, _, _, _ = cast(blueprint)
    morning = [{"name": "テスA", "kind": "スライム", "color": (1, 2, 3), "hp": 4, "max_hp": 10, "happy": 50}]
    evening = [{"name": "テスA", "kind": "スライム", "color": (1, 2, 3), "hp": 9, "max_hp": 10, "happy": 70}]
    LAST_CALLS.clear()
    png = OUTPUT / "ranch_times.png"
    saved = png.read_bytes() if png.exists() else None   # 君の新聞を、チェックの間だけ預かる
    if png.exists():
        png.unlink()
    path, error = try_quietly(lambda: publish(morning, evening, a))
    made = png.exists() and png.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    if saved is not None:
        png.write_bytes(saved)
    elif png.exists():
        png.unlink()   # チェック用の新聞は、残さない
    if error is not None:
        return False, f"publish でエラーが出たよ → {type(error).__name__}: {error}"
    if not LAST_CALLS:
        return False, "save_newspaper(morning, evening, mvp) を呼ぼう"
    if len(LAST_CALLS) != 1:
        return False, "save_newspaper は、1回だけ呼ぼう"
    given = LAST_CALLS[0]
    if not (given[0] is morning and given[1] is evening and given[2] is a):
        return False, "朝の記録 → 夕方の記録 → MVP の順番で渡そう"
    if not path:
        return False, "save_newspaper の答え（画像の場所）を return しよう"
    if not made:
        return False, "新聞の画像ができていないみたい"
    return True, "新聞（PNG）を発行できた"


def check_todos(blueprint, trainer_class, prepare_teams, run_morning, choose_mvp, publish):
    """TODOができたか、ふるまいを見て調べる。"""
    checks = [
        check_todo1(blueprint, trainer_class, prepare_teams),
        check_todo2(blueprint, trainer_class, run_morning),
        check_todo3(blueprint, choose_mvp),
        check_todo4(blueprint, publish),
    ]
    return show_report(checks, "これまでの部品を組み合わせて、牧場の1日を新聞にできた！ 第2部、完走おめでとう！🏆")
