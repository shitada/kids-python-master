# 🎨 ドットえメーカー
# すうじの ならびを いろに かえて、PNG がぞうを つくるよ。
#
# やりかた:
#   1. 下の # TODO の ところを かく
#   2. じっこうすると、おなじ フォルダに art.png が できる
#   3. art.png を クリックして みてね！

from PIL import Image, ImageDraw

# いろの ばんごう → RGB（あか, みどり, あお それぞれ 0〜255）の じしょ
palette = {
    0: (255, 255, 255),  # しろ
    1: (0, 0, 0),        # くろ
    2: (255, 90, 95),    # あか
    3: (255, 214, 0),    # きいろ
    4: (0, 175, 240),    # みずいろ
    5: (120, 200, 80),   # みどり
}

# えの せっけいず（二次元リスト）。すうじ = いろの ばんごう。
# これは「ハート」だよ。すきに かきかえてね！
grid = [
    [0, 2, 2, 0, 2, 2, 0],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [0, 2, 2, 2, 2, 2, 0],
    [0, 0, 2, 2, 2, 0, 0],
    [0, 0, 0, 2, 0, 0, 0],
]

CELL = 40  # 1ますを なんピクセルの 四角に するか


def check_grid(grid):
    """すべての ぎょうの ながさが おなじか しらべる。"""
    width = len(grid[0])
    for row in grid:
        if len(row) != width:
            print("⚠️ ぎょうの ながさが そろっていないよ。おなじ かずに してね。")
            return False
    return True


def make_art(grid, filename="art.png"):
    if not check_grid(grid):
        return

    rows = len(grid)
    cols = len(grid[0])
    image = Image.new("RGB", (cols * CELL, rows * CELL), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 二重ループで 1ますずつ いろを ぬろう！
    for row in range(rows):
        for col in range(cols):
            # TODO: ここを かいてみよう！（4つの ヒントの とおりに）
            # ヒント1: いまの ますの すうじ →  number = grid[row][col]
            # ヒント2: その すうじの いろ    →  color = palette[number]
            # ヒント3: ぬる ばしょ（ひだり上）→  x = col * CELL,  y = row * CELL
            # ヒント4: 四角を ぬる →
            #     draw.rectangle([x, y, x + CELL, y + CELL], fill=color)
            pass

    image.save(filename)
    print(f"✅ できたよ！ {filename} を クリックして みてね。")


make_art(grid)
