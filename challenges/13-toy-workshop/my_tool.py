# 🛠️ 第13章 君だけの道具工房
# 何を覚えて、何ができる道具にする？ 自分で設計した道具を、牧場で使おう！
#
# 進め方:
#   1. 下の「設計メモ」を読んで（変えてもOK）、TODO を番号順に直す
#   2. 保存して ▷ ボタン（または python my_tool.py）で実行
#   3. 君の道具が動くようすと「TODOチェック」を見てみよう
#
# モンスターの設計図は monster.py（読んでOK）、絵やチェックの道具は ranch_tools.py（さわらなくてOK）。

from monster import Monster
from ranch_tools import check_todos, run_chapter, show_design, show_results, title, try_use


# ===== 🚨 事件のコード（読むだけ。直さなくていいよ） =====

class TrainerWithCounters:
    """道具の残り回数を、トレーナーが全部覚えている設計図。"""

    def __init__(self, name):
        self.name = name
        self.team = []
        self.bell_left = 2        # ベルの残り回数
        self.whistle_left = 3     # 笛の残り回数
        self.ribbon_left = 1      # リボンの残り回数
        self.drum_left = 5        # たいこの残り回数 …道具が増えるたびに、ここが増える！


# ===== 君が書くところ =====

# 🛠️ 設計メモ（name・icon・max_uses は自由に書きかえてOK。effect は自由改造で変えよう）
DESIGN = {
    "name": "おやつベル",   # 道具の名前
    "icon": "🔔",           # 道具の絵文字
    "max_uses": 2,          # 何回使えるか
    "effect": "eat",        # モンスターに頼む仕事: "eat"（食べる）/ "play"（遊ぶ）/ "sleep"（眠る）
}


class MyToy:
    """君が設計した道具。使える回数が決まっている。"""

    def __init__(self, name, max_uses):
        self.icon = DESIGN["icon"]
        # TODO 1: 名前 self.name、使える回数 self.max_uses、
        #         残り回数 self.left（はじめは max_uses と同じ）を用意しよう。
        self.name = name

    def use(self, monster):
        """monster に使う。使えたら True、使えなかったら False を返す。"""
        # TODO 2: 残り回数が 0 なら、何もしないで False を返そう。
        #         残っていたら、monster に食べてもらって（effect が "eat" だからね。量は自由）、
        #         残り回数を 1 へらして、True を返そう。
        return False   # ← ここを直そう

    def refill(self):
        """残り回数を、使える回数（max_uses）までもどす。"""
        # TODO 3: 残り回数を、満タンにもどそう。
        pass   # ← ここを直そう


def calc_fee(monster):
    """牧場の温泉の入場料。つかれている子は半額の 25円、それ以外は 50円。"""
    # TODO 4: monster がつかれていたら 25、そうでなければ 50 を return しよう。
    #         （覚えておくことがない計算なので、クラスにしない！ ふつうの関数で十分）
    return 0   # ← ここを直そう


# ===== 第10章で完成させた道具たち（読んでOK） =====

class Ball:
    def __init__(self):
        self.name = "ボール"
        self.icon = "🎾"

    def use(self, monster):
        if monster.is_tired():
            return False
        monster.play()
        return True


class Snack:
    def __init__(self, amount):
        self.name = "おやつ"
        self.icon = "🍪"
        self.amount = amount

    def use(self, monster):
        monster.eat(self.amount)
        return True


def use_all(tools, monster):
    results = []
    for tool in tools:
        results.append(tool.use(monster))
    return results


# ===== ここから下は完成済み（読んでOK） =====

def main():
    title("🚨 事件発生！")
    mina = TrainerWithCounters("ミナ")
    print(f"🔎 ミナが覚えていること: {vars(mina)}")
    print("😱 道具が増えるたびに、トレーナーの属性が増えていく！ 第04章の「変数だらけ」に逆もどり……")

    title("📝 君の設計メモ")
    show_design(DESIGN)

    title("🛠️ 工房で、道具を2つ作ったよ")
    toy_a = MyToy(DESIGN["name"], DESIGN["max_uses"])
    toy_b = MyToy(DESIGN["name"], DESIGN["max_uses"])
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    piko.stay_up_late()
    for count in range(DESIGN["max_uses"] + 1):
        try_use(toy_a, piko, "A")
    try_use(toy_b, piko, "B", check_only=True)
    print("🔋 A を補充！")
    toy_a.refill()
    try_use(toy_a, piko, "A", check_only=True)

    title("🧰 道具箱リレー")
    momo = Monster("モモ", "おばけ", (255, 160, 200))
    tools = [Ball(), Snack(2), toy_b]
    results = use_all(tools, momo)
    show_results(tools, results)

    title("♨️ 温泉の入場料")
    gabu = Monster("ガブ", "ドラゴン", (120, 200, 90))
    gabu.stay_up_late()
    gabu.stay_up_late()
    for member in [momo, gabu]:
        print(f"   {member.name}（HP {member.hp}）→ {calc_fee(member)}円")


def check():
    return check_todos(MyToy, calc_fee, DESIGN, Monster)


if __name__ == "__main__":
    run_chapter(main, check)   # main を動かして、そのあと TODO チェックをするよ
