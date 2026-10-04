# 🎒 第09章 トレーナーとチーム
# トレーナーが、モンスターのチームを持つ！ 号令ひとつで、チーム全員をお世話しよう。
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python trainer_team.py）で実行
#   3. チームのようすと「TODOチェック」を見てみよう
#
# モンスターの設計図は、同じフォルダの monster.py に入っているよ（第08章の完成版。読んでOK）。
# 絵を出したりTODOをチェックしたりする道具は ranch_tools.py。そっちは、さわらなくてOK。

from monster import Monster
from ranch_tools import check_todos, first_match, names, run_chapter, show_hp, show_slots, title


def already_here(ranch, monster):
    """monster と同じ本人が ranch にいれば True、いなければ False を返す。（第07章で作ったもの）"""
    for member in ranch:
        if member is monster:
            return True
    return False


# ===== 🚨 事件のコード（読むだけ。直さなくていいよ） =====

class BrokenTrainer:
    """トレーナーの設計図……のつもり。チーム表の作り方が、どこかおかしい！"""
    team = []

    def __init__(self, name):
        self.name = name

    def recruit(self, monster):
        self.team.append(monster)


# ===== 君が書くところ =====

class Trainer:
    """トレーナーの設計図。モンスターのチームを持っている。"""

    def __init__(self, name):
        self.name = name
        self.max_team = 3       # チームに入れるのは3匹まで
        # TODO 1: このトレーナー専用のチーム表（空っぽのリスト）を、self.team に用意しよう。
        self.team = None   # ← ここを直そう

    def recruit(self, monster):
        """monster をチームに迎える。入れたら True、入れなかったら False を返す。"""
        # TODO 2: 同じ本人がもうチームにいたら、False を返そう（already_here を使おう）。
        #         チームがもういっぱい（max_team 匹）なら、False を返そう。
        #         どちらでもなければ、monster をチームに append して、True を返そう。
        return False   # ← ここを直そう

    def care_all(self, amount):
        """チームの全員に、amount ずつごはんをあげる。"""
        # TODO 3: 自分のチームの1匹ずつに、eat(amount) を頼もう。
        pass   # ← ここを直そう

    def show_team(self):
        """チームのメンバーを、番号つきで紹介する。"""
        print(f"🎒 {self.name} のチーム")
        # TODO 4: 1匹ずつ「   1. ピコ（スライム）……」のように、番号と自己紹介を表示しよう。
        #         だれもいなければ「   （まだ仲間がいない）」と表示しよう。


# ===== ここから下は完成済み（読んでOK） =====

def scout(trainer, monster):
    """trainer が monster をスカウトする。"""
    if trainer.recruit(monster):
        print(f"✅ {monster.name} が、{trainer.name} のチームに入った！")
    elif not isinstance(trainer.team, list):
        print(f"🥚 {trainer.name} は、まだチーム表を持っていない……（TODO 1）")
    elif already_here(trainer.team, monster):
        print(f"🛑 {monster.name} は、もう {trainer.name} のチームにいるよ！")
    elif len(trainer.team) >= trainer.max_team:
        print(f"🛑 {trainer.name} のチームは、もういっぱい！ {monster.name} は入れない（{trainer.max_team}匹まで）")
    else:
        print(f"🛑 {monster.name} は入れなかった……？（TODO 2）")


def main():
    title("🚨 事件発生！")
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    broken_mina = BrokenTrainer("ミナ")
    broken_ryo = BrokenTrainer("リョウ")
    print("ミナが ピコ をスカウト！")
    broken_mina.recruit(piko)
    print(f"📋 ミナのチーム:   {names(broken_mina.team)}")
    print(f"📋 リョウのチーム: {names(broken_ryo.team)}")
    print("😱 え？ リョウは、まだだれもスカウトしていないのに！")

    title("🏡 トレーナー登録")
    mina = Trainer("ミナ")
    ryo = Trainer("リョウ")
    gabu = Monster("ガブ", "ドラゴン", (120, 200, 90))
    popo = Monster("ポポ", "スライム", (250, 220, 90))
    nana = Monster("ナナ", "おばけ", (200, 170, 255))
    momo = Monster("モモ", "おばけ", (255, 160, 200))
    print(f"🧑 {mina.name} と {ryo.name} が、トレーナーになった！")
    print("🐲 スカウトを待っている子: ピコ・ガブ・ポポ・ナナ・モモ")

    title("🔍 スカウトタイム")
    scout(mina, piko)
    scout(mina, gabu)
    scout(mina, piko)
    scout(ryo, momo)
    scout(mina, popo)
    scout(mina, nana)
    print()
    show_slots(mina)
    show_slots(ryo)

    title("🌳 チームのお世話")
    piko.stay_up_late()
    gabu.play()
    momo.stay_up_late()
    print("\nミナ「みんな、ごはんだよ！」")
    mina.care_all(3)
    print()
    show_hp(mina)
    show_hp(ryo)

    title("🪪 チーム紹介")
    mina.show_team()
    print()
    ryo.show_team()
    print()
    sora = Trainer("ソラ")   # 今日トレーナーになったばかりのソラ
    sora.show_team()

    title("🤝 先鋒どうしの交流戦")
    first_match(mina, ryo)


def check():
    return check_todos(Trainer, Monster)


if __name__ == "__main__":
    run_chapter(main, check)   # main を動かして、そのあと TODO チェックをするよ
