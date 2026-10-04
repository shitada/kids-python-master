# 🛡️ 第12章 親の仕事に、ひと工夫（完成例）
# バリアを持つモンスター「ガード」を作ろう。親の仕事を使って、自分の仕事を足すよ！
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python shield_monster.py）で実行
#   3. バリアのゲージと「TODOチェック」を見てみよう
#
# モンスターの設計図は monster.py（読んでOK）、絵やチェックの道具は ranch_tools.py（さわらなくてOK）。

from monster import Monster
from ranch_tools import attack_demo, check_todos, run_chapter, show_guard, title, try_demo


# ===== 🚨 事件のコード（読むだけ。直さなくていいよ） =====

class BrokenShield(Monster):
    """バリアを持つモンスター……のつもり。誕生セット係に、どこか足りないところがある！"""

    def __init__(self, name, kind, color):
        self.shield = 2


# ===== 君が書くところ =====

class ShieldMonster(Monster):
    """バリアで、ダメージを少しへらせるモンスター。"""

    def __init__(self, name, kind, color):
        # TODO 1: 親（Monster）の __init__ に、name・kind・color を渡して、誕生の準備をしてもらおう。
        super().__init__(name, kind, color)

        # TODO 2: このモンスターだけの属性、バリアの残り回数 self.shield を 2 にしよう。
        self.shield = 2

    def take_damage(self, amount):
        """バリアがあれば、ダメージを1へらして受ける。本当に減った量を返す。"""
        # TODO 3: amount が 0 より大きくて、バリアが残っていたら（self.shield > 0）、
        #         amount を 1 へらして、バリアを 1 使おう。
        if amount > 0 and self.shield > 0:
            amount = amount - 1
            self.shield = self.shield - 1

        # TODO 4: 親（Monster）の take_damage に amount を渡して、その答えを return しよう。
        return super().take_damage(amount)


# ===== 第11章までに完成させたもの（読んでOK） =====

class FloatingMonster(Monster):
    """ふわふわ浮かぶモンスター。遊んでも、あまりつかれない。"""

    def play(self):
        before = self.hp
        self.happy = self.happy + 10
        if self.happy > 100:
            self.happy = 100
        self.hp = self.hp - 1
        if self.hp < 0:
            self.hp = 0
        print(f"☁️  {self.name} は ふわふわ遊んだ！ ごきげん {self.happy}  HP {before} → {self.hp}")

    def is_tired(self):
        return self.hp <= 1


# ===== ここから下は完成済み（読んでOK） =====

def main():
    title("🚨 事件発生！")
    broken = BrokenShield("ガード", "スライム", (170, 170, 190))
    print(f"🔎 vars でのぞくと: {vars(broken)}")
    print("🍎 ガード「おなかすいた！ ごはんを食べよう」")
    try_demo(lambda: broken.eat(3))
    print("😱 バリアは持っているのに、HP がない！？")

    title("🛡️ ガードの誕生")
    guard = ShieldMonster("ガード", "スライム", (170, 170, 190))
    show_guard(guard)

    title("🥊 練習試合: モモ VS ガード")
    momo = Monster("モモ", "おばけ", (255, 160, 200))
    attack_demo(momo, guard, times=3)

    title("☁️ フワも、たいあたりを受けてみる")
    fuwa = FloatingMonster("フワ", "おばけ", (230, 230, 255))
    lost = fuwa.take_damage(5)
    print(f"💥 フワ に 5 のたいあたり！ 本当に減ったのは {lost}  HP 10 → {fuwa.hp}")
    print("   （フワは take_damage を書きかえていないので、親のルールのまま。バリアもない）")


def check():
    return check_todos(Monster, ShieldMonster)


if __name__ == "__main__":
    run_chapter(main, check)   # main を動かして、そのあと TODO チェックをするよ
