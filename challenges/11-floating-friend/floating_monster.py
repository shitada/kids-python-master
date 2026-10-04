# 👻 第11章 ふわふわな仲間
# Monster の設計図を受けついで、遊び方だけちがう「フワ」を誕生させよう！
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python floating_monster.py）で実行
#   3. フワとピコのちがいと「TODOチェック」を見てみよう
#
# モンスターの設計図は monster.py（読んでOK）、絵やチェックの道具は ranch_tools.py（さわらなくてOK）。

from monster import Monster
from ranch_tools import check_todos, draw_faces, run_chapter, show_team_hp, title, try_hatch


# ===== 🚨 事件のコード（読むだけ。直さなくていいよ） =====

class CopiedFuwa:
    """フワ用に、Monster の設計図をまるごと写した……つもりのもの（一部だけ見せるよ）"""

    def __init__(self, name, kind, color):
        self.name = name
        self.kind = kind
        self.hp = 10
        self.happy = 50

    def play(self):
        self.happy = self.happy + 10
        self.hp = self.hp - 3        # 古いルールのまま！ 0 で止める行がない


# ===== 君が書くところ =====

# TODO 1: FloatingMonster を、Monster を受けつぐ設計図にしよう。
#         class の行の、名前のうしろに (Monster) を書くよ。
class FloatingMonster:   # ← ここを直そう
    """ふわふわ浮かぶモンスター。遊んでも、あまりつかれない。"""

    # TODO 3: play を書きかえよう。
    #         ごきげんを 10 増やして（100 まで）、HP は 1 だけ減らす（0 まで）。
    #         monster.py の Monster.play と同じ形で、最初に before = self.hp とメモしておこう。
    #         遊んだ時のメッセージは、これを使ってね:
    #         print(f"☁️  {self.name} は ふわふわ遊んだ！ ごきげん {self.happy}  HP {before} → {self.hp}")

    # TODO 4: is_tired を書きかえよう。HP が 1 以下なら True。


def hatch_fuwa():
    """フワを誕生させて返す。"""
    # TODO 2: FloatingMonster から、名前 "フワ"、種族 "おばけ" の子を誕生させて return しよう。
    #         色は好きな RGB でOK。
    return None   # ← ここを直そう


# ===== 第10章までに完成させたもの（読んでOK） =====

class Ball:
    """ボール。元気な子に、遊んでもらう道具。"""

    def __init__(self):
        self.name = "ボール"
        self.icon = "🎾"

    def use(self, monster):
        if monster.is_tired():
            return False
        monster.play()
        return True


def already_here(ranch, monster):
    for member in ranch:
        if member is monster:
            return True
    return False


class Trainer:
    """トレーナーの設計図。モンスターのチームを持っている。"""

    def __init__(self, name):
        self.name = name
        self.max_team = 3
        self.team = []

    def recruit(self, monster):
        if already_here(self.team, monster):
            return False
        if len(self.team) >= self.max_team:
            return False
        self.team.append(monster)
        return True

    def use_on_team(self, tool):
        for member in self.team:
            tool.use(member)


# ===== ここから下は完成済み（読んでOK） =====

def main():
    title("🚨 事件発生！")
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    copied = CopiedFuwa("フワ（コピー）", "おばけ", (230, 230, 255))
    for count in range(1, 5):
        piko.play()
        copied.play()
        print(f"   {count}回目 → {copied.name} HP {copied.hp}\n")
    print("😱 ピコは 0 で止まったのに、コピーしたフワは HP がマイナス！")
    print("   Monster の play は直したのに、コピーの方は古いルールのままだった……")

    title("🥚 フワの誕生")
    fuwa = try_hatch(hatch_fuwa)
    if fuwa is None:
        return
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    draw_faces([piko, fuwa])
    print(f"自己紹介: {fuwa}")
    print("👀 FloatingMonster には __init__ も __str__ も書いていないのに、ちゃんと動いた！")
    fuwa.stay_up_late()
    fuwa.eat(2)

    title("🎾 ミナ「みんな、ボールで遊ぼう！」")
    mina = Trainer("ミナ")
    mina.recruit(piko)
    mina.recruit(fuwa)
    piko.take_damage(4)      # ピコも午前中の練習で、HP 6 になった
    show_team_hp(mina)
    for round_number in range(1, 3):
        print(f"\n--- {round_number}回目 ---")
        mina.use_on_team(Ball())
        show_team_hp(mina)
    print("\n✨ 同じボール、同じ号令。でも、遊び方とつかれ方は、その子しだい！")


def check():
    return check_todos(Monster, FloatingMonster, hatch_fuwa)


if __name__ == "__main__":
    run_chapter(main, check)   # main を動かして、そのあと TODO チェックをするよ
