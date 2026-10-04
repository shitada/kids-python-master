"""🐲 モンスターの設計図（第08章で完成させたもの）

読んでOK、直さなくてOK！
第09章では、この設計図から生まれたモンスターたちを、トレーナーがチームに迎えるよ。
"""


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

    def can_play_with(self, other):
        """other といっしょに遊べるか、True か False で答える。"""
        if self is other:
            return False

        if self.is_tired() or other.is_tired():
            return False

        return True

    def play_with(self, other):
        """other と遊ぶ。遊べたら True、お休みなら False を返す。"""
        if not self.can_play_with(other):
            return False
        self.play()
        other.play()
        return True

    def tackle(self, other):
        """other に、たいあたりする。相手の HP が本当に減った量を返す。"""
        power = self.power_against(other)
        return other.take_damage(power)
