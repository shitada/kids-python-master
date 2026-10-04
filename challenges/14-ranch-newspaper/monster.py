"""🧰 部品箱（第04〜13章で完成させたもの、全部入り）

読んでOK、直さなくてOK！
Monster・FloatingMonster・ShieldMonster・Ball・MyToy・Trainer が入っているよ。
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


# ===== 第09〜13章で完成させた部品 =====

class FloatingMonster(Monster):              # 第11章
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


class ShieldMonster(Monster):                # 第12章
    def __init__(self, name, kind, color):
        super().__init__(name, kind, color)
        self.shield = 2

    def take_damage(self, amount):
        if amount > 0 and self.shield > 0:
            amount = amount - 1
            self.shield = self.shield - 1
        return super().take_damage(amount)


class Ball:                                  # 第10章
    def __init__(self):
        self.name = "ボール"
        self.icon = "🎾"

    def use(self, monster):
        if monster.is_tired():
            return False
        monster.play()
        return True


class MyToy:                                 # 第13章（おやつベル）
    def __init__(self, name, max_uses):
        self.name = name
        self.icon = "🔔"
        self.max_uses = max_uses
        self.left = max_uses

    def use(self, monster):
        if self.left == 0:
            return False
        monster.eat(3)
        self.left = self.left - 1
        return True


class Trainer:                               # 第09章・第10章
    def __init__(self, name):
        self.name = name
        self.max_team = 3
        self.team = []

    def recruit(self, monster):
        for member in self.team:
            if member is monster:
                return False
        if len(self.team) >= self.max_team:
            return False
        self.team.append(monster)
        return True

    def care_all(self, amount):
        for member in self.team:
            member.eat(amount)

    def use_on_team(self, tool):
        for member in self.team:
            tool.use(member)
