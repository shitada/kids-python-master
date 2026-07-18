# 🎨 ドットえメーカー（かんせいれい）
# すうじの ならびを いろに かえて、PNG がぞうを つくるよ。

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

    # 二重ループで 1ますずつ いろを ぬる
    for row in range(rows):
        for col in range(cols):
            number = grid[row][col]          # いまの ますの すうじ
            color = palette[number]          # その すうじの いろ
            x = col * CELL                   # ぬる ばしょ（よこ）
            y = row * CELL                   # ぬる ばしょ（たて）
            draw.rectangle([x, y, x + CELL, y + CELL], fill=color)

    image.save(filename)
    print(f"✅ できたよ！ {filename} を クリックして みてね。")


make_art(grid)
