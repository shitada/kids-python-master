# 🍎 第05章 わざをおぼえる（完成例）
# モンスターに「できること（メソッド）」を教えて、牧場の1日を過ごそう！
#
# 進め方:
#   1. 下の「① 君が書くところ」の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python monster_care.py）で実行
#   3. HPバーやごきげんバーの動きと「TODOチェック」を見てみよう
#
# 「② さわらなくていいところ」は、絵やバーを出すための道具。読まなくてもOK。


# ===== ① 君が書くところ =====

class Monster:
    """モンスターの設計図。「覚えていること」と「できること」をまとめて書く。"""

    def __init__(self, name, kind, color):
        # 第04章で作った「誕生セット係」。少しだけ属性が増えたよ。
        self.name = name
        self.kind = kind
        self.color = color
        self.level = 1
        self.max_hp = 10        # 🆕 HPの上限（これより多くはならない）
        self.hp = self.max_hp   # 生まれた時は、HP満タン
        self.happy = 50         # 🆕 ごきげん（0〜100）

    # ----- お手本のメソッド（もう完成しているよ） -----

    def show(self):
        """自分の顔と、HP・ごきげんを表示する。"""
        draw_face(self.kind, self.color)
        print(f"   {self.name}（{self.kind}）Lv.{self.level}")
        print(f"   HP       {bar(self.hp, self.max_hp, HP_COLOR)} {self.hp}/{self.max_hp}")
        print(f"   ごきげん {bar(self.happy, 100, HAPPY_COLOR)} {self.happy}/100\n")

    def sleep(self):
        """ぐっすり眠って、HPが満タンになる。"""
        self.hp = self.max_hp
        print(f"💤 {self.name} は すやすや…… HP が満タンになった！")

    # ----- 君が完成させるメソッド -----

    def eat(self, amount):
        """ごはんを食べて、HPが amount だけ回復する。"""
        before = self.hp
        # TODO 1: HP を amount だけ増やそう。
        #         でも、max_hp より大きくなったら、max_hp にそろえてね。
        self.hp = self.hp + amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        print(f"🍎 {self.name} は もぐもぐ…… HP {before} → {self.hp}")

    def play(self):
        """元気に遊ぶ。ごきげんが上がるけれど、HPが減る。"""
        before = self.hp
        # TODO 2: ごきげん（happy）を 10 増やそう。ただし 100 より大きくしない。
        #         HP を 3 減らそう。ただし 0 より小さくしない。
        self.happy = self.happy + 10
        if self.happy > 100:
            self.happy = 100
        self.hp = self.hp - 3
        if self.hp < 0:
            self.hp = 0

        print(f"⚽ {self.name} は 元気に遊んだ！ ごきげん {self.happy}  HP {before} → {self.hp}")

    def is_tired(self):
        """つかれているかどうかを、True か False で答える。"""
        # TODO 3: HP が 3 以下なら True、そうでなければ False を返そう。
        return self.hp <= 3


def main():
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    momo = Monster("モモ", "おばけ", (255, 160, 200))

    print("☀️  朝の牧場\n")
    piko.show()
    momo.show()

    print("🍽️  朝ごはんの時間")
    momo.hp = 4   # モモは夜ふかしして、おなかペコペコ（お話の準備のため、ここだけ直接書きかえているよ）
    momo.eat(3)
    momo.eat(5)   # 上限を超えないかな？
    piko.eat(5)   # ピコはもう満タンだけど……？

    print("\n🌳 ピコの1日")
    for hour in range(1, 5):
        print(f"--- {hour}時間目 ---")
        # TODO 4: ピコに遊んでもらおう。そのあと、つかれていたら寝かせよう。
        #   使うメソッド: piko.play()   piko.is_tired()   piko.sleep()
        piko.play()
        if piko.is_tired():
            piko.sleep()

    print("\n🌙 夜の牧場\n")
    piko.show()
    momo.show()

    check_todos(Monster, piko)


# ===== ② さわらなくていいところ =====
# ここから下は、色つきの絵やバーを出したり、TODOをチェックしたりする道具だよ。
# 興味があれば読んでもOK。でも、今回の勉強に必要なのは上の①だけ。

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


def quietly(action):
    """action を、画面に何も出さずに実行する（チェック用）。"""
    with contextlib.redirect_stdout(io.StringIO()):
        return action()


def check_todos(blueprint, piko):
    """TODOができたか、モンスターのふるまいを見て調べる。"""
    print("\n📋 TODOチェック")
    results = []

    test = blueprint("テスト", "スライム", (1, 2, 3))
    test.hp = 5
    quietly(lambda: test.eat(3))
    first = test.hp
    quietly(lambda: test.eat(100))
    ok1 = first == 8 and test.hp == test.max_hp
    results.append(ok1)
    if ok1:
        print("  ✅ TODO 1 クリア！ ごはんで回復して、上限も守れた")
    elif first == 5:
        print("  🔧 TODO 1 まだ: ごはんを食べても HP が増えていないよ")
    elif first < 8:
        print("  🔧 TODO 1 まだ: 食べた分を「足して」いないみたい。self.hp = self.hp + amount の形かな？")
    else:
        print("  🔧 TODO 1 まだ: たくさん食べた時に、HP が max_hp を超えていないかな？")

    test.hp = 10
    test.happy = 95
    quietly(test.play)
    happy_ok = test.happy == 100
    hp_ok = test.hp == 7
    test.hp = 2
    quietly(test.play)
    floor_ok = test.hp == 0
    ok2 = happy_ok and hp_ok and floor_ok
    results.append(ok2)
    if ok2:
        print("  ✅ TODO 2 クリア！ ごきげんは100まで、HPは0まで")
    elif not hp_ok:
        print("  🔧 TODO 2 まだ: 遊んだ後、HP が 3 減っていないよ")
    elif not happy_ok:
        print("  🔧 TODO 2 まだ: ごきげんが 10 増えていないか、100 を超えているよ")
    else:
        print("  🔧 TODO 2 まだ: HP がマイナスになっていないかな？")

    test.hp = 3
    tired_low = quietly(test.is_tired)
    test.hp = 4
    tired_high = quietly(test.is_tired)
    ok3 = tired_low is True and tired_high is False
    results.append(ok3)
    if ok3:
        print("  ✅ TODO 3 クリア！ つかれているか、正しく答えられた")
    elif tired_low is None:
        print("  🔧 TODO 3 まだ: return がないみたい。print ではなく return で答えよう")
    elif tired_high is None:
        print("  🔧 TODO 3 まだ: HP 4 の時に何も返していない（None）よ。else: return False を足そう")
    else:
        print("  🔧 TODO 3 まだ: HP 3 の時に True、HP 4 の時に False になるかな？")

    # 遊んだだけなら HP は 1 以下になる。つかれていない時に眠ると HP 10・ごきげん 90 になる。
    played = piko.happy >= 80
    slept = piko.hp > 1
    slept_too_much = piko.hp == piko.max_hp and piko.happy == 90
    ok4 = played and slept and not slept_too_much
    results.append(ok4)
    if ok4:
        print("  ✅ TODO 4 クリア！ ピコは遊んで、つかれた時だけ眠れた")
    elif not (ok1 and ok2 and ok3):
        print("  🔧 TODO 4 まだ: さきに TODO 1〜3 を完成させてから、もう一度実行してね")
    elif not played:
        print("  🔧 TODO 4 まだ: ピコが1時間ごとに遊んでいないみたい")
    elif not slept:
        print("  🔧 TODO 4 まだ: ピコがヘトヘト……piko.is_tired() で確かめて、つかれたら眠らせよう")
    else:
        print("  🔧 TODO 4 まだ: つかれていない時も眠っているみたい。is_tired の後ろの ( ) を確かめよう")

    if all(results):
        print("\n🎉 全部クリア！ モンスターに「できること」を教えられるようになった！")
    elif os.environ.get("STRICT_CHECK"):
        sys.exit(1)


if __name__ == "__main__":
    main()
