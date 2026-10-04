# 🍎 第05章 わざをおぼえる（完成例）
# モンスターに「できること（メソッド）」を教えて、牧場の1日を過ごそう！
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python monster_care.py）で実行
#   3. HPバーやごきげんバーの動きと「TODOチェック」を見てみよう
#
# 絵やバーを出したりTODOをチェックしたりする道具は、同じフォルダの ranch_tools.py に入っているよ。
# そっちは、さわらなくてOK。

from ranch_tools import HAPPY_COLOR, HP_COLOR, bar, check_todos, draw_face


# ===== 君が書くところ =====

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

    def stay_up_late(self):
        """夜ふかしして、HPが6減る。でも 0 より小さくはならない。"""
        self.hp = self.hp - 6
        if self.hp < 0:
            self.hp = 0
        print(f"🌙 {self.name} は 夜ふかしした…… HP が {self.hp} になった")

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
    momo.stay_up_late()   # モモは夜ふかしして、おなかペコペコ
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

if __name__ == "__main__":
    main()
