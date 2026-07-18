# 🥁 かだい02: メトロノーム　むずかしさ ★★☆

**テンポ**（はやさ）に あわせて、リズムを きざむ どうぐを つくろう！
がめんに `★`（つよい はく）と `・`（よわい はく）が、テンポどおりに ながれるよ。

## 🎯 この かだいで できるように なること
- くりかえし（ループ）で リズムを きざむ
- じかんを あつかう（`time.sleep`）
- けいさん: **1はくの びょうすう = 60 ÷ BPM**
- あまり `%` で「なんはくに 1かい つよく」を つくる

---

## 🧩 しくみ

- **BPM** … 1ぷんかんに なんかい うつか（おおきいほど はやい）
- **1ぷん = 60びょう** だから → **1はく = 60 ÷ BPM びょう**
  - れい: BPM 60 なら 1はく = 1びょう。BPM 120 なら 1はく = 0.5びょう。
- **4びょうし** は、`beat` を `4` で わった **あまりが 0** のとき つよい はく！

```
はく: 1  2  3  4  5  6  7  8
      ★  ・  ・  ・  ★  ・  ・  ・
```

---

## 🚀 やってみよう

1. `metronome.py` を ひらく
2. `# TODO` の 2つを、ヒントを みながら なおす
3. ▷ ボタン（または `python metronome.py`）で じっこう
4. `★ ・ ・ ・` が テンポどおりに ながれたら せいこう！🎉

> ⏱ とちゅうで とめたい ときは、ターミナルで **Ctrl + C**。
> `BPM` を `60` や `180` に かえて、はやさの ちがいを かんじてみよう！

---

## 🌟 はってん チャレンジ

- `BEATS` を `3` に かえて、**ワルツ**（3びょうし）に してみよう
- `TOTAL` を おおきくして、ながく ならしてみよう
- （じょうきゅう）**おとの ファイル（.wav）** を つくって、ダウンロードして きこう！

### 🔊 じょうきゅう: クリックおんを つくる（numpy）

Codespaces では おとを その場で ならせないけど、
**.wav ファイルを つくって ダウンロード** すれば きけるよ。
下を あたらしい ファイル（`click_wav.py`）に コピーして じっこうしてね。

```python
import numpy as np
import wave

BPM = 90
rate = 44100                    # おとの こまかさ
beat = 60 / BPM                 # 1はくの びょうすう
total = 8

samples = np.zeros(int(rate * beat * total))
for i in range(total):
    start = int(rate * beat * i)
    length = int(rate * 0.05)   # 0.05びょうの みじかい「カチッ」
    freq = 1500 if i % 4 == 0 else 900   # つよい はくは たかい おと
    t = np.arange(length) / rate
    samples[start:start + length] = 0.5 * np.sin(2 * np.pi * freq * t)

data = (samples * 32767).astype(np.int16)
with wave.open("click.wav", "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(rate)
    w.writeframes(data.tobytes())
print("✅ click.wav を つくったよ！ ダウンロードして きいてね。")
```
