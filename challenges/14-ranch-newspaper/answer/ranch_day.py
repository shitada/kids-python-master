# 📰 第14章 牧場の1日を新聞に（完成例）
# これまでの仲間と道具が全員集合！ 牧場の1日を動かして、ドット絵入りの新聞を作ろう。
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python ranch_day.py）で実行
#   3. 牧場の1日と、output フォルダにできる新聞（ranch_times.png）を見てみよう
#
# これまでに作った部品は、全部 monster.py に入っているよ（読んでOK）。
# 絵やチェックの道具は ranch_tools.py（さわらなくてOK）。

from monster import Ball, FloatingMonster, Monster, MyToy, ShieldMonster, Trainer
from ranch_tools import (check_todos, print_newspaper, run_chapter, save_newspaper,
                         show_teams, take_record, title)


# ===== 🚨 事件のコード（読むだけ。直さなくていいよ） =====

def broken_record(monsters):
    """朝のようすを記録する……つもりのコード。"""
    return list(monsters)          # 本人の名札を、そのまま並べているだけ！


# ===== 君が書くところ =====

def prepare_teams(mina, ryo, piko, fuwa, guard, momo, gabu):
    """2人のトレーナーに、チームを作ってもらう。"""
    # TODO 1: ミナのチームに ピコ・フワ・ガード、リョウのチームに モモ・ガブ を、
    #         この順番で迎えよう（トレーナーの recruit に頼もう）。
    mina.recruit(piko)
    mina.recruit(fuwa)
    mina.recruit(guard)
    ryo.recruit(momo)
    ryo.recruit(gabu)


def run_morning(trainer, toy):
    """朝のお世話。トレーナーに号令をかけてもらう。"""
    # TODO 2: まず trainer の care_all で、全員に 2 ずつごはん。
    #         次に trainer の use_on_team で、全員に toy を使おう。
    trainer.care_all(2)
    trainer.use_on_team(toy)


def choose_mvp(monsters):
    """いちばんごきげんな子（本人）を返す。同じなら先にいた子。だれもいなければ None。"""
    # TODO 3: 第07章の weakest と、同じ形で書けるよ。
    if len(monsters) == 0:
        return None
    best = monsters[0]
    for member in monsters:
        if member.happy > best.happy:
            best = member
    return best


def publish(morning, evening, mvp):
    """新聞を発行する。できた画像の場所を返す。"""
    # TODO 4: save_newspaper に、朝の記録・夕方の記録・MVP を、この順番で渡して、
    #         その答え（画像の場所）を return しよう。
    return save_newspaper(morning, evening, mvp)


# ===== ここから下は完成済み（読んでOK） =====

def main():
    title("🚨 事件発生！")
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    piko.stay_up_late()
    morning_news = broken_record([piko])
    print(f"☀️  朝の記録: ピコ HP {morning_news[0].hp}")
    piko.eat(2)
    print(f"🌙 夕方のピコ: HP {piko.hp}")
    print(f"📰 朝の記事を読みかえすと…… ピコ HP {morning_news[0].hp}")
    print("😱 朝の記事まで、夕方の HP になってる！？")

    title("🏡 全員集合！")
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    fuwa = FloatingMonster("フワ", "おばけ", (230, 230, 255))
    guard = ShieldMonster("ガード", "スライム", (170, 170, 190))
    momo = Monster("モモ", "おばけ", (255, 160, 200))
    gabu = Monster("ガブ", "ドラゴン", (120, 200, 90))
    mina = Trainer("ミナ")
    ryo = Trainer("リョウ")
    prepare_teams(mina, ryo, piko, fuwa, guard, momo, gabu)
    show_teams([mina, ryo])
    piko.stay_up_late()                       # ピコは、今日も夜ふかしあけ……
    everyone = mina.team + ryo.team

    title("☀️ 朝の記録")
    morning = take_record(everyone)           # その時の数字を「写して」記録する係

    title("🌅 朝のお世話")
    run_morning(mina, MyToy("おやつベル", 3))
    run_morning(ryo, MyToy("おやつベル", 3))

    title("🌞 午後: ボール大会")
    for round_number in range(1, 4):
        print(f"--- ミナのチーム {round_number}回目 ---")
        mina.use_on_team(Ball())
    print("--- リョウのチーム ---")
    ryo.use_on_team(Ball())

    title("🌙 夕方の記録")
    evening = take_record(everyone)
    mvp = choose_mvp(everyone)

    title("📰 新聞を発行！")
    print_newspaper(morning, evening, mvp)
    path = publish(morning, evening, mvp)
    if path:
        print(f"\n🖼️  新聞の画像ができたよ → {path}")
        print("    左のファイル一覧で output フォルダを開いて、クリックしてみよう！")


def check():
    return check_todos(Monster, Trainer, prepare_teams, run_morning, choose_mvp, publish)


if __name__ == "__main__":
    run_chapter(main, check)   # main を動かして、そのあと TODO チェックをするよ
