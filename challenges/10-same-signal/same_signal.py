# 🎾 第10章 みんな同じ合図で
# ボール・おやつ・パズル……。種類がちがう道具を、同じ「use」の合図で使おう！
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python same_signal.py）で実行
#   3. 道具を使うようすと「TODOチェック」を見てみよう
#
# モンスターの設計図は monster.py（読んでOK）、絵やチェックの道具は ranch_tools.py（さわらなくてOK）。

from monster import Monster
from ranch_tools import balloon_finale, check_todos, new_balloon, run_chapter, show_results, show_team_hp, title


# ===== 🚨 事件のコード（読むだけ。直さなくていいよ） =====

def broken_use(tool_name, monster):
    """受付係: 道具の名前を調べて、使い方を決める。"""
    if tool_name == "ボール":
        monster.play()
    elif tool_name == "おやつ":
        monster.eat(3)
    elif tool_name == "パズル":       # ← パズルを足した！
        monster.play()
        monster.eat(1)


def broken_hand_out(trainer, tool_name):
    """配る係: チーム全員に、道具を使う。"""
    for member in trainer.team:
        if tool_name == "ボール":
            member.play()
        elif tool_name == "おやつ":
            member.eat(3)
        # ← パズルを足すのを、忘れている！


# ===== 君が書くところ =====

class Ball:
    """ボール。元気な子に、遊んでもらう道具。（お手本・完成済み）"""

    def __init__(self):
        self.name = "ボール"
        self.icon = "🎾"

    def use(self, monster):
        """monster に使う。使えたら True、使えなかったら False を返す。"""
        if monster.is_tired():
            return False
        monster.play()
        return True


class Snack:
    """おやつ。食べると HP が回復する道具。"""

    def __init__(self, amount):
        self.name = "おやつ"
        self.icon = "🍪"
        self.amount = amount

    def use(self, monster):
        """monster に使う。使えたら True、使えなかったら False を返す。"""
        # TODO 1: monster に self.amount ぶん食べてもらって、True を返そう。
        return False   # ← ここを直そう


class Puzzle:
    """パズル。考えて遊んだあと、ごほうびを一口もらえる道具。"""

    def __init__(self):
        self.name = "パズル"
        self.icon = "🧩"

    def use(self, monster):
        """monster に使う。使えたら True、使えなかったら False を返す。"""
        # TODO 2: monster がつかれていたら、何もしないで False を返そう。
        #         元気なら、play() してから eat(1) して、True を返そう。
        return False   # ← ここを直そう


def use_all(tools, monster):
    """tools の道具を、順番に全部 monster に使う。それぞれの答え（True/False）をリストで返す。"""
    # TODO 3: 1つずつ tool.use(monster) して、その答えを results に入れていこう。
    results = []

    return results


# ===== 第09章で完成させたもの（＋今回1つ足す） =====

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

    def care_all(self, amount):
        for member in self.team:
            member.eat(amount)

    def use_on_team(self, tool):
        """🆕 チームの全員に、同じ道具を1回ずつ使う。"""
        # TODO 4: 自分のチームの1匹ずつに、tool.use(その子) を頼もう。
        pass   # ← ここを直そう


# ===== ここから下は完成済み（読んでOK） =====

def main():
    title("🚨 事件発生！")
    mina = Trainer("ミナ")
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    gabu = Monster("ガブ", "ドラゴン", (120, 200, 90))
    momo = Monster("モモ", "おばけ", (255, 160, 200))
    for member in [piko, gabu, momo]:
        mina.recruit(member)
    print("🧩 受付係「ピコ、パズルをどうぞ！」")
    broken_use("パズル", piko)
    print("\n🎒 配る係「ミナのチームのみんな、パズルをどうぞ！」")
    broken_hand_out(mina, "パズル")
    print("   ……（シーン）")
    print("😱 受付係は直したのに、配る係はパズルを知らない！")

    title("🎒 道具袋の中身を、ピコに使おう")
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    tools = [Ball(), Snack(3), Puzzle()]
    results = use_all(tools, piko)
    show_results(tools, results)

    title("🧩 ミナ「みんな、パズルだよ！」")
    mina = Trainer("ミナ")
    for member in [piko, gabu, momo]:
        mina.recruit(member)
    momo.stay_up_late()
    momo.stay_up_late()      # モモは、2日つづけて夜ふかし……
    print()
    mina.use_on_team(Puzzle())
    print()
    show_team_hp(mina)

    title("🎈 新しい道具が届いた！")
    balloon = new_balloon()   # ranch_tools.py の中で作られた、だれも知らない道具
    print(f"{balloon.icon} {balloon.name} …… use_all も Trainer も、この道具のことを知らない。でも……")
    print()
    show_results([balloon], use_all([balloon], piko))
    mina.use_on_team(balloon)
    balloon_finale(balloon)


def check():
    return check_todos(Monster, Snack, Puzzle, use_all, Trainer)


if __name__ == "__main__":
    run_chapter(main, check)   # main を動かして、そのあと TODO チェックをするよ
