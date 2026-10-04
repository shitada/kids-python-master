# 🪪 第06章 自己紹介カード
# モンスターが print で自己紹介できるようにして、牧場の事件を解決しよう！
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python monster_card.py）で実行
#   3. 画面の表示と「TODOチェック」を見てみよう
#
# 絵やバーを出したりTODOをチェックしたりする道具は、同じフォルダの ranch_tools.py に入っているよ。
# そっちは、さわらなくてOK。

from ranch_tools import HAPPY_COLOR, HP_COLOR, bar, check_todos, draw_face, introduce, show_clues, title, try_zukan


# ===== 君が書くところ =====

class Monster:
    """モンスターの設計図。第05章で完成させたメソッドが、もう入っているよ。"""

    def __init__(self, name, kind, color):
        self.name = name
        self.kind = kind
        self.color = color
        self.level = 1
        self.max_hp = 10
        self.hp = self.max_hp
        self.happy = 50

    # TODO 1: 自己紹介メソッド __str__ を作ろう。
    #   下の2行の先頭の「# 」を消して、return の文字を完成させてね。
    #   例: ピコ（スライム）Lv.1  HP 10/10  ごきげん 50
    # def __str__(self):
    #     return "ここに自己紹介の文字"

    def show(self):
        """自分の顔と、HP・ごきげんを表示する。"""
        draw_face(self.kind, self.color)
        print(f"   {self.name}（{self.kind}）Lv.{self.level}")
        print(f"   HP       {bar(self.hp, self.max_hp, HP_COLOR)} {self.hp}/{self.max_hp}")
        print(f"   ごきげん {bar(self.happy, 100, HAPPY_COLOR)} {self.happy}/100\n")

    def sleep(self):
        self.hp = self.max_hp
        print(f"💤 {self.name} は すやすや…… HP が満タンになった！")

    def stay_up_late(self):
        """夜ふかしして、HPが6減る。でも 0 より小さくはならない。"""
        self.hp = self.hp - 6
        if self.hp < 0:
            self.hp = 0
        print(f"🌙 {self.name} は 夜ふかしした…… HP が {self.hp} になった")

    def eat(self, amount):
        before = self.hp
        self.hp = self.hp + amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"🍎 {self.name} は もぐもぐ…… HP {before} → {self.hp}")

    def play(self):
        before = self.hp
        self.hapy = self.happy + 10
        if self.happy > 100:
            self.happy = 100
        self.hp = self.hp - 3
        if self.hp < 0:
            self.hp = 0
        print(f"⚽ {self.name} は 元気に遊んだ！ ごきげん {self.happy}  HP {before} → {self.hp}")

    def is_tired(self):
        return self.hp <= 3


def print_zukan(monsters):
    """牧場の子を、図鑑のように番号つきで1匹ずつ表示する。"""
    print("📖 モンスター図鑑")
    number = 1
    for monster in monsters:
        # TODO 4: 「No.1 ピコ（スライム）Lv.1 ……」のように、番号と自己紹介を表示しよう。
        #   ヒント: f文字列の { } の中に monster を入れると、__str__ が使われるよ。

        number = number + 1


def main():
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    momo = Monster("モモ", "おばけ", (255, 160, 200))
    gabu = Monster("ガブ", "ドラゴン", (120, 200, 90))
    ranch = [piko, momo, gabu]

    title("📸 自己紹介タイム")
    piko.show()
    introduce(piko)    # ← TODO 1 の前と後で、ここの表示が変わるよ（中身は print(piko) と同じ）
    introduce(momo)

    title("🚨 事件発生！")
    print("「モモと遊んでも、ごきげんが上がらないんです！」と、牧場のスタッフが困っている。")
    momo.play()
    momo.play()
    introduce(momo)

    title("🔎 ルーペで調査")
    # TODO 2: 下の {} を vars(momo) に変えて、モモの中身（属性）を全部のぞこう。
    clues = {}
    show_clues(clues)
    # TODO 3: 犯人が分かったら、Monster の設計図の中のまちがいを直そう。

    title("🧪 なにもの？")
    print("type(piko)      →", type(piko))
    print("type(piko.name) →", type(piko.name))
    print("type(piko.hp)   →", type(piko.hp))
    print("type(ranch)     →", type(ranch))

    title("📖 図鑑づくり")
    try_zukan(print_zukan, ranch)
    print()
    print("🧪 実験: リストをまるごと print すると……")
    print(ranch)

    check_todos(Monster, ranch, clues, momo, print_zukan)

if __name__ == "__main__":
    main()
