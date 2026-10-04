# 🥚 第04章 はじめての1匹（完成例）
# モンスターの「設計図（クラス）」を作って、牧場に1匹目を誕生させよう！
#
# 進め方:
#   1. 下の TODO を、番号順に直す
#   2. 保存して ▷ ボタン（または python first_monster.py）で実行
#   3. ターミナルにモンスターの顔と「TODOチェック」が出るよ
#
# 絵を出したりTODOをチェックしたりする道具は、同じフォルダの ranch_tools.py に入っているよ。
# そっちは、さわらなくてOK。

from ranch_tools import check_todos, show_level, show_monster


# ===== 君が書くところ =====

class Monster:
    """モンスターの設計図。「モンスターは何を覚えているか」をここに書く。"""

    def __init__(self, name, kind, color):
        # 生まれた瞬間に、自動で1回だけ動く「誕生セット係」。
        # self は「いま生まれている、その1匹」のこと。
        self.name = name        # お手本: 「この子の名前」の箱に、受け取った name を入れる

        # TODO 1: お手本と同じように、kind（種族）と color（色）を
        #         この子の持ち物（属性）にしよう。
        self.kind = kind
        self.color = color

        # TODO 2: どの子も、生まれた時の HP は 10 にしよう。
        #         下の self.level のように、引数で受け取らない属性も作れるよ。
        #         （「入れる」は = が1つ。== は「同じ？」とたずねる記号だよ）
        self.hp = 10

        self.level = 1          # お手本: どの子もレベル1から始まる


def main():
    print("🏡 モンスター牧場に、タマゴが届いた！\n")

    # 1匹目（お手本）: 設計図 Monster から、本物の1匹を誕生させる
    piko = Monster("ピコ", "スライム", (90, 200, 250))

    # TODO 3: 2匹目を誕生させよう。None を消して Monster(...) を書く。
    #   種族は "スライム" "ドラゴン" "おばけ" から選べるよ。
    #   色は課題01と同じ RGB（赤, 緑, 青）。それぞれ 0〜255。
    buddy = Monster("モモ", "おばけ", (255, 160, 200))

    show_monster(piko)
    show_monster(buddy)

    # TODO 4: ピコだけ、レベルを1上げよう。下の行の「+ 0」を直してね。
    #   実行する前に予想！ レベルが変わるのは、ピコ？ 2匹目？ 両方？
    piko.level = piko.level + 1

    print("⭐ レベルアップの結果")
    show_level(piko)
    show_level(buddy)

    check_todos(Monster, piko, buddy)

if __name__ == "__main__":
    main()
