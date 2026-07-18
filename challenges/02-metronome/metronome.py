# 🥁 メトロノーム
# テンポ（はやさ）に あわせて、リズムを きざむ どうぐ。
#
# やりかた:
#   1. 下の # TODO を 2つ なおす
#   2. じっこうすると ★ ・ ・ ・ が テンポどおりに ながれる
#   3. とめたい ときは Ctrl + C

import time
import sys

BPM = 90    # テンポ（1ぷんかんの ビートの かず。おおきいほど はやい）
BEATS = 4   # なんびょうしか（4 = 4びょうし）
TOTAL = 8   # なんはく ならすか


def run(bpm, beats, total, wait=True):
    # TODO1: 1はくは なんびょう？
    # ヒント: 1ぷん(60びょう)に bpm かい うつよ。 60 ÷ bpm
    seconds_per_beat = 0  # ← ここを なおそう！（60 / bpm）

    print(f"🥁 BPM={bpm} / {beats}びょうし で {total}はく いくよ！")
    for beat in range(total):
        # TODO2: 4はくに 1かい ★（つよい はく）に したい。
        # ヒント: beat を beats で わった "あまり" が 0 のとき
        if False:  # ← ここを なおそう！（beat % beats == 0）
            print(f"{beat + 1:>2}  ★ イチ！")   # つよい はく
        else:
            print(f"{beat + 1:>2}  ・")          # よわい はく

        if wait:
            time.sleep(seconds_per_beat)

    print("おわり！ 👏")


fast = "--fast" in sys.argv   # --fast をつけると またずに かくにん できる
run(BPM, BEATS, TOTAL, wait=not fast)
