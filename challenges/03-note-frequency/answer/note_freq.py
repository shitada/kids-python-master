# 🎸 ドレミ → しゅうはすう けいさんき（かんせいれい）
# おとの たかさ（しゅうはすう Hz）を けいさんするよ。

# きじゅんの おと: ラ(A4) = 440 Hz
BASE_FREQ = 440

# おとの なまえ → きじゅん(ラ)から なんはんおん はなれているか の じしょ
semitones = {
    "ド":   -9,
    "レ":   -7,
    "ミ":   -5,
    "ファ": -4,
    "ソ":   -2,
    "ラ":    0,
    "シ":    2,
    "ド↑":   3,
}


def to_freq(name):
    n = semitones[name]   # ラから なんはんおん はなれているか

    # 平均律: 1オクターブ(12はんおん)で しゅうはすうは ちょうど 2ばい
    freq = BASE_FREQ * (2 ** (n / 12))

    return round(freq, 1)   # みやすく、小数第1いちまで


print("🎵 ドレミの しゅうはすう（Hz）")
print("-" * 24)
for name in semitones:
    print(f"  {name:<3}  {to_freq(name):>7} Hz")
