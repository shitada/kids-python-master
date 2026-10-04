# 🐣 第07章 にぎやかな牧場
# タマゴがたくさん届いた！ 仲間を増やして、「その子」を選んでお世話しよう。
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python busy_ranch.py）で実行
#   3. 画面の名簿と「TODOチェック」を見てみよう
#
# 絵を出したりTODOをチェックしたりする道具は、同じフォルダの ranch_tools.py に入っているよ。
# そっちは、さわらなくてOK。

from ranch_tools import check_todos, deliver_eggs, draw_faces, hp_line, run_chapter, show_roster, title


# ===== 第06章までに完成させた設計図（今回は直さなくてOK） =====

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


# ===== 🚨 事件のコード（読むだけ。直さなくていいよ） =====

def broken_hatch(eggs):
    """タマゴを全部ふ化させる……つもりのコード。どこかがおかしい！"""
    ranch = []
    monster = Monster("？", "スライム", (90, 200, 250))
    for egg in eggs:
        monster.name = egg["name"]
        print(f"🐣 {egg['name']} が生まれた！")
        ranch.append(monster)
    return ranch


# ===== 君が書くところ =====

def hatch_one(egg):
    """タマゴ1個（辞書）から、新しいモンスターを1匹誕生させて返す。"""
    # TODO 1: egg["name"]、egg["kind"]、egg["color"] を使って、
    #         新しい Monster を誕生させて return しよう。
    return None   # ← ここを直そう


def already_here(ranch, monster):
    """monster と同じ本人が ranch にいれば True、いなければ False を返す。"""
    # TODO 2: ranch の子を1匹ずつ見て、monster と「同じ本人」なら True を返そう。
    #         最後まで見つからなかったら False を返そう。
    return False   # ← ここを直そう


def weakest(ranch):
    """ranch の中で、HP がいちばん低い子（本人）を返す。だれもいなければ None。"""
    # TODO 3: HP の数字ではなく、「その子」を返そう。
    #         HP が同じ子がいたら、先に名簿にいた子を返そう。
    return None   # ← ここを直そう


def feed_all(ranch, amount):
    """ranch の全員に、amount ずつごはんをあげる。"""
    # TODO 4: 1匹ずつ、その子の eat に頼もう。
    pass   # ← ここを直そう


# ===== ここから下は完成済み（読んでOK） =====

def welcome(ranch, newcomer):
    """新しい子を名簿に入れる。同じ本人が、もういたら断る。"""
    if already_here(ranch, newcomer):
        print(f"🛑 {newcomer.name} は、もう名簿にいるよ！（同じ子に、名札が2まいついていただけ）")
    else:
        ranch.append(newcomer)
        print(f"✅ {newcomer.name}（{newcomer.kind}）を名簿に入れた！")


def main():
    title("🚨 事件発生！")
    demo_eggs = [
        {"name": "ポコ", "kind": "スライム", "color": (250, 220, 90)},
        {"name": "ミミ", "kind": "おばけ", "color": (200, 170, 255)},
        {"name": "ルル", "kind": "ドラゴン", "color": (250, 120, 90)},
    ]
    broken = broken_hatch(demo_eggs)
    print("\n📋 できあがった名簿:")
    for monster in broken:
        print(f"   ・{monster.name}")
    print("😱 3匹生まれたはずなのに、全員ルル……？")

    title("🏡 いつもの牧場")
    piko = Monster("ピコ", "スライム", (90, 200, 250))
    momo = Monster("モモ", "おばけ", (255, 160, 200))
    ranch = [piko, momo]
    piko.stay_up_late()   # 先輩のピコは、昨日の夜ふかしでヘトヘト

    title("📦 タマゴ便が届いた！")
    newcomers = []
    for egg in deliver_eggs():
        baby = hatch_one(egg)
        if baby is None:
            print(f"🥚 {egg['name']} のタマゴは、まだ割れない……（TODO 1）")
            continue
        newcomers.append(baby)
        welcome(ranch, baby)
    draw_faces(newcomers)

    print("🏷️  受付に「guest」という名札の子が来た。")
    guest = piko
    welcome(ranch, guest)

    title("📋 牧場の名簿")
    show_roster(ranch)

    title("🎉 歓迎会！ みんなで遊ぼう")
    for member in ranch:
        member.play()

    title("🍎 みんなでごはん")
    feed_all(ranch, 2)

    title("🩺 いちばん弱っている子を、助けよう")
    patient = weakest(ranch)
    if patient is None:
        print("🔍 まだ見つけられない……（TODO 3）")
    else:
        print(f"😿 いちばん弱っている子は…… {patient}")
        patient.sleep()

    print()
    for member in ranch:
        print("   " + hp_line(member))


def check():
    return check_todos(Monster, hatch_one, already_here, weakest, feed_all)


if __name__ == "__main__":
    run_chapter(main, check)   # main を動かして、そのあと TODO チェックをするよ
