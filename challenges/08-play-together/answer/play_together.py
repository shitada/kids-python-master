# 🤝 第08章 となりの子とあそぼう（完成例）
# モンスター同士で遊んだり、たいあたり勝負をしたりしよう！
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python play_together.py）で実行
#   3. 広場のようすと、運動会と、「TODOチェック」を見てみよう
#
# 絵を出したり、対決を進めたり、TODOをチェックしたりする道具は、
# 同じフォルダの ranch_tools.py に入っているよ。そっちは、さわらなくてOK。

from ranch_tools import battle, check_todos, hp_line, run_chapter, title

# どの種族が、どの種族に強いか（スライム → ドラゴン → おばけ → スライム）
STRONG_AGAINST = {"スライム": "ドラゴン", "ドラゴン": "おばけ", "おばけ": "スライム"}


class Monster:
    """モンスターの設計図。"""

    def __init__(self, name, kind, color):
        self.name = name
        self.kind = kind
        self.color = color
        self.level = 1
        self.max_hp = 10
        self.hp = self.max_hp
        self.happy = 50

    # ----- 第06章までに完成させたメソッド（今回は直さなくてOK） -----

    def __str__(self):
        return f"{self.name}（{self.kind}）Lv.{self.level}  HP {self.hp}/{self.max_hp}  ごきげん {self.happy}"

    def sleep(self):
        self.hp = self.max_hp
        print(f"💤 {self.name} は すやすや…… HP が満タンになった！")

    def stay_up_late(self):
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
        self.happy = self.happy + 10
        if self.happy > 100:
            self.happy = 100
        self.hp = self.hp - 3
        if self.hp < 0:
            self.hp = 0
        print(f"⚽ {self.name} は 元気に遊んだ！ ごきげん {self.happy}  HP {before} → {self.hp}")

    def is_tired(self):
        return self.hp <= 3

    # ----- 🆕 お手本のメソッド（もう完成しているよ） -----

    def take_damage(self, amount):
        """ダメージを受ける。HP は 0 より小さくならない。本当に減った量を返す。"""
        before = self.hp
        self.hp = self.hp - amount
        if self.hp < 0:
            self.hp = 0
        return before - self.hp

    def power_against(self, other):
        """相手（other）の種族を見て、たいあたりの強さを決める。"""
        if STRONG_AGAINST.get(self.kind) == other.kind:
            return 5    # 相手に強い！
        if STRONG_AGAINST.get(other.kind) == self.kind:
            return 2    # 相手に弱い……
        return 3        # ふつう

    # ----- 君が完成させるメソッド -----

    def can_play_with(self, other):
        """other といっしょに遊べるか、True か False で答える。"""
        # TODO 1: other が自分自身（同じ本人）なら、False を返そう。
        if self is other:
            return False

        # TODO 2: 自分か相手の、どちらかがつかれていたら、False を返そう。
        if self.is_tired() or other.is_tired():
            return False

        return True

    def play_with(self, other):
        """other と遊ぶ。遊べたら True、お休みなら False を返す。"""
        # TODO 3: can_play_with で確かめて、遊べる時だけ、
        #         自分の play() と、相手の play() を1回ずつ呼んで、True を返そう。
        #         遊べない時は、だれも遊ばずに False を返そう。
        if self.can_play_with(other):
            self.play()
            other.play()
            return True
        return False

    def tackle(self, other):
        """other に、たいあたりする。相手の HP が本当に減った量を返す。"""
        # TODO 4: power_against で強さを決めて、相手の take_damage に頼もう。
        #         take_damage が返した数（本当に減った量）を、そのまま返そう。
        power = self.power_against(other)
        return other.take_damage(power)


# ===== 🚨 事件のコード（読むだけ。直さなくていいよ） =====

def broken_referee(target, damage):
    """運動会の審判……のつもりのコード。相手の HP を、直接書きかえている！"""
    target.hp = target.hp - damage


# ===== ここから下は完成済み（読んでOK） =====

def invite(first, second):
    """first が second を遊びにさそう。"""
    print(f"🤝 {first.name} → {second.name}：いっしょに遊ぼう！")
    if first.play_with(second):
        print("   🎉 ふたり遊び、成功！\n")
    elif first is second:
        print("   🛑 自分とは、ふたり遊びできないよ\n")
    elif first.is_tired() or second.is_tired():
        print("   🛑 つかれている子がいるので、今回はお休み\n")
    else:
        print("   🛑 お休み……？ ふたりとも元気なのに（TODO 3）\n")


def main():
    title("🚨 事件発生！")
    momo = Monster("モモ", "おばけ", (255, 160, 200))
    momo.stay_up_late()
    print("審判「たいあたり、6 ダメージ！」")
    broken_referee(momo, 6)
    print("   " + hp_line(momo))
    print("😱 HP がマイナスになっちゃった！ 牧場のルール（0 より小さくしない）はどこへ……？")

    print("\n🩹 お手本の take_damage に頼むと……")
    nana = Monster("ナナ", "おばけ", (200, 170, 255))
    nana.stay_up_late()
    lost = nana.take_damage(6)
    print(f"   本当に減った量: {lost}")
    print("   " + hp_line(nana))

    title("🌳 ふたり遊びの広場")
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    momo = Monster("モモ", "おばけ", (255, 160, 200))
    gabu = Monster("ガブ", "ドラゴン", (120, 200, 90))
    momo.stay_up_late()
    print()
    invite(piko, momo)
    invite(gabu, momo)
    invite(piko, piko)
    invite(gabu, piko)
    for member in [piko, momo, gabu]:
        print("   " + hp_line(member))

    title("🏟️ たいあたり運動会")
    sura = Monster("スラ太", "スライム", (110, 220, 210))
    doran = Monster("ドラン", "ドラゴン", (250, 120, 90))
    print("ドラン「試合の前に、ウォーミングアップだ！」")
    doran.play()
    print()
    battle(sura, doran)


def check():
    return check_todos(Monster)


if __name__ == "__main__":
    run_chapter(main, check)   # main を動かして、そのあと TODO チェックをするよ
