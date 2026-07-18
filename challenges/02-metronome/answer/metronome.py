# 🥁 メトロノーム（かんせいれい）
# テンポ（はやさ）に あわせて、リズムを きざむ どうぐ。

import time
import sys

BPM = 90    # テンポ（1ぷんかんの ビートの かず。おおきいほど はやい）
BEATS = 4   # なんびょうしか（4 = 4びょうし）
TOTAL = 8   # なんはく ならすか


def run(bpm, beats, total, wait=True):
    seconds_per_beat = 60 / bpm   # 1はくの びょうすう

    print(f"🥁 BPM={bpm} / {beats}びょうし で {total}はく いくよ！")
    for beat in range(total):
        if beat % beats == 0:
            print(f"{beat + 1:>2}  ★ イチ！")   # つよい はく
        else:
            print(f"{beat + 1:>2}  ・")          # よわい はく

        if wait:
            time.sleep(seconds_per_beat)

    print("おわり！ 👏")


fast = "--fast" in sys.argv   # --fast をつけると またずに かくにん できる
run(BPM, BEATS, TOTAL, wait=not fast)
