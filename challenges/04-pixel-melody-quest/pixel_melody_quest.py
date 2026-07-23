"""Pixel Melody Quest - 12個のTODOを順番に完成させよう。"""

import math

import numpy as np
import pygame


WIDTH = 960
HEIGHT = 640
FPS = 60
BPM = 100

EXPLORE = "explore"
RHYTHM = "rhythm"
CLEAR = "clear"

INK = (31, 37, 45)
PAPER = (235, 239, 232)
MIST = (85, 95, 96)
WHITE = (255, 255, 255)
HEART = (245, 86, 98)
GOLD = (255, 215, 76)

# 音の名前、周波数、色、位置
NOTE_SPECS = [
    ("DO", 261.6, (242, 89, 97), (100, 120)),
    ("RE", 293.7, (247, 148, 67), (260, 190)),
    ("MI", 329.6, (249, 211, 72), (470, 145)),
    ("FA", 349.2, (114, 196, 104), (730, 115)),
    ("SO", 392.0, (71, 177, 210), (160, 410)),
    ("LA", 440.0, (102, 126, 234), (510, 420)),
    ("SI", 493.9, (180, 105, 211), (790, 410)),
]

MELODY = ["DO", "RE", "MI", "SO", "MI", "RE", "DO", "DO"]

# 課題01と同じように、数字と色でピコを描く。
PLAYER_GRID = [
    [0, 0, 1, 1, 1, 0, 0],
    [0, 1, 2, 2, 2, 1, 0],
    [1, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 2, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 1],
    [0, 1, 2, 1, 2, 1, 0],
    [0, 0, 1, 2, 1, 0, 0],
    [0, 1, 1, 0, 1, 1, 0],
]

PLAYER_PALETTE = {
    0: None,
    1: INK,
    2: (99, 205, 222),
    3: WHITE,
}


def initialize_pygame():
    """pygameを準備する。音が使えなくてもゲームは遊べる。"""
    pygame.display.init()
    pygame.font.init()

    audio_error = None
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    except pygame.error as error:
        audio_error = str(error)
        print(f"Sound disabled: {audio_error}")

    return audio_error


def draw_pixel_grid(surface, grid, palette, rect):
    """二次元リストを四角いドット絵として描く。"""
    rows = len(grid)
    cols = len(grid[0])
    cell = min(rect.width // cols, rect.height // rows)
    width = cols * cell
    height = rows * cell
    start_x = rect.centerx - width // 2
    start_y = rect.bottom - height

    for row_index, row in enumerate(grid):
        for col_index, number in enumerate(row):
            color = palette[number]
            if color is None:
                continue
            pixel = pygame.Rect(
                start_x + col_index * cell,
                start_y + row_index * cell,
                cell,
                cell,
            )
            pygame.draw.rect(surface, color, pixel)


class ToneBank:
    """音の名前を受け取り、短い音を鳴らす。"""

    SAMPLE_RATE = 44100
    DURATION = 0.18

    def __init__(self, enabled):
        self.enabled = enabled
        self.sounds = {}
        if not self.enabled:
            return

        frequencies = {name: frequency for name, frequency, _, _ in NOTE_SPECS}
        for name, frequency in frequencies.items():
            self.sounds[name] = self._make_tone(frequency)

    def _make_tone(self, frequency):
        sample_count = int(self.SAMPLE_RATE * self.DURATION)
        time_axis = np.arange(sample_count, dtype=np.float32) / self.SAMPLE_RATE
        wave = np.sin(2 * math.pi * frequency * time_axis)
        envelope = np.linspace(1.0, 0.0, sample_count, dtype=np.float32)
        samples = (wave * envelope * 0.25 * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(samples)

    def play(self, name):
        if self.enabled:
            self.sounds[name].play()


class Actor:
    """動く登場人物の基本となる設計図。"""

    def __init__(self, x, y, width, height, color):
        # TODO 01: 位置・大きさ・色を、このインスタンスに覚えさせよう。
        # ヒント:
        #   self.rect = pygame.Rect(x, y, width, height)
        #   self.color = color
        self.rect = pygame.Rect(x, y, 1, 1)
        self.color = MIST

    def draw(self, surface, now):
        del now
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)


class Player(Actor):
    """自分で操作する主人公「ピコ」。"""

    def __init__(self, x, y):
        # TODO 02: Actorの設計図を受け継いで、ピコを作ろう。
        # ヒント: super().__init__(x, y, 42, 48, (99, 205, 222))
        super().__init__(x, y, 14, 16, MIST)
        self.start_position = (x, y)
        self.speed = 4
        self.max_hearts = 3
        self.hearts = self.max_hearts
        self.invincible_until = 0

    def draw(self, surface, now):
        if now < self.invincible_until and (now // 100) % 2 == 0:
            return

        # TODO 03: 四角ではなく、二次元リストのドット絵でピコを描こう。
        # ヒント: draw_pixel_grid(surface, PLAYER_GRID, PLAYER_PALETTE, self.rect)
        super().draw(surface, now)

    def update(self, keys):
        dx = 0
        dy = 0

        # TODO 04: 押されたキーに合わせて、dx と dyを変えよう。
        # ヒント:
        #   左: dx -= self.speed    右: dx += self.speed
        #   上: dy -= self.speed    下: dy += self.speed
        #   keys[pygame.K_LEFT]や keys[pygame.K_a]で調べられる。

        self.move(dx, dy)

    def move(self, dx, dy):
        if dx and dy:
            dx = round(dx * 0.71)
            dy = round(dy * 0.71)
        self.rect.move_ip(dx, dy)
        self.keep_in_forest()

    def keep_in_forest(self):
        # TODO 05: ピコを常に画面の中へ戻そう。
        # ヒント: self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        pass

    def take_damage(self, now):
        if now < self.invincible_until:
            return False

        self.hearts -= 1
        self.invincible_until = now + 1200
        if self.hearts <= 0:
            self.respawn(now)
        return True

    def respawn(self, now):
        self.rect.topleft = self.start_position
        self.hearts = self.max_hearts
        self.invincible_until = now + 1600


class NoteSpirit:
    """集めると色と音を取り戻せる音符の精霊。"""

    def __init__(self, name, frequency, color, position):
        # TODO 06: 精霊ごとに違う属性を覚えさせよう。
        # ヒント: name、frequency、colorをそのまま self.○○に入れる。
        # rectは pygame.Rect(position[0], position[1], 30, 38)
        # 最初はまだ集めていないので、collectedは False。
        self.name = "DO"
        self.frequency = 0.0
        self.color = MIST
        self.rect = pygame.Rect(position[0], position[1], 30, 38)
        self.collected = True

    def collect(self):
        if self.collected:
            return False
        self.collected = True
        return True

    def draw(self, surface, now):
        if self.collected:
            return

        bob = round(math.sin(now / 240 + self.rect.x) * 4)
        center = (self.rect.centerx, self.rect.centery + bob)
        pygame.draw.circle(surface, (*self.color, 55), center, 25)
        pygame.draw.circle(surface, self.color, center, 11)
        pygame.draw.rect(
            surface,
            self.color,
            (center[0] + 8, center[1] - 24, 5, 25),
        )
        pygame.draw.line(
            surface,
            self.color,
            (center[0] + 12, center[1] - 23),
            (center[0] + 22, center[1] - 18),
            4,
        )


def make_note_spirits():
    # TODO 07: NOTE_SPECSから7体の NoteSpiritを作り、リストで返そう。
    # ヒント:
    # return [
    #     NoteSpirit(name, frequency, color, position)
    #     for name, frequency, color, position in NOTE_SPECS
    # ]
    return [NoteSpirit(*NOTE_SPECS[0])]


def collect_touching_note(player, notes, tone_bank):
    # TODO 08: ピコとぶつかった精霊の collect()を呼ぼう。
    # collect()が Trueなら tone_bank.play(note.name)で音を鳴らし、
    # その noteを returnする。見つからなければ Noneを returnする。
    return None


class NoiseMonster:
    """音と色を邪魔するノイズモンスター。"""

    def __init__(self, x, y, velocity):
        self.rect = pygame.Rect(x, y, 46, 36)
        self.velocity = velocity
        self.color = (116, 73, 137)

    def update(self):
        # TODO 09: velocityの値だけ横へ動き、端では正負を反対にしよう。
        # ヒント:
        #   self.rect.x += self.velocity
        #   画面の端なら self.velocity *= -1
        pass

    def draw(self, surface):
        points = [
            (self.rect.left, self.rect.centery),
            (self.rect.left + 8, self.rect.top),
            (self.rect.centerx, self.rect.top + 6),
            (self.rect.right - 8, self.rect.top),
            (self.rect.right, self.rect.centery),
            (self.rect.right - 8, self.rect.bottom),
            (self.rect.centerx, self.rect.bottom - 6),
            (self.rect.left + 8, self.rect.bottom),
        ]
        pygame.draw.polygon(surface, self.color, points)
        pygame.draw.circle(surface, WHITE, (self.rect.x + 15, self.rect.y + 15), 4)
        pygame.draw.circle(surface, WHITE, (self.rect.x + 31, self.rect.y + 15), 4)
        pygame.draw.circle(surface, INK, (self.rect.x + 16, self.rect.y + 16), 2)
        pygame.draw.circle(surface, INK, (self.rect.x + 30, self.rect.y + 16), 2)


def handle_noise_hit(player, monsters, now):
    # TODO 10: ぶつかったモンスターがいたら player.take_damage(now)を呼ぼう。
    # ダメージを受けたら True、誰にもぶつからなければ Falseを返す。
    return False


class MelodyTree:
    """7つの音がそろうと開くメロディの木。"""

    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 55, 30, 110, 125)
        self.opened = False

    def update(self, collected_count, total_count):
        self.opened = collected_count == total_count

    def can_start(self, player):
        return self.opened and self.rect.inflate(90, 70).colliderect(player.rect)

    def draw(self, surface):
        trunk = (126, 81, 52) if self.opened else (92, 89, 84)
        leaves = (76, 181, 105) if self.opened else (102, 108, 105)
        pygame.draw.rect(surface, trunk, (self.rect.centerx - 14, 85, 28, 70))
        pygame.draw.circle(surface, leaves, (self.rect.centerx, 70), 48)
        pygame.draw.circle(surface, leaves, (self.rect.centerx - 35, 85), 35)
        pygame.draw.circle(surface, leaves, (self.rect.centerx + 35, 85), 35)
        if self.opened:
            pygame.draw.circle(surface, GOLD, self.rect.center, 66, 4)


class RhythmChallenge:
    """BPMに合わせたスペースキー入力を判定する。"""

    COUNTDOWN_MS = 1000
    HIT_WINDOW_MS = 320
    REQUIRED_HITS = 6

    def __init__(self, tone_bank, bpm=BPM):
        self.tone_bank = tone_bank
        self.bpm = bpm

        # TODO 11: 1拍が何ミリ秒か計算しよう。
        # 課題02の「1拍 = 60 / BPM」と、1秒 = 1000ミリ秒を使う。
        # ヒント: round(60_000 / bpm)
        self.beat_ms = 1000

        self.sequence = MELODY
        self.started_at = 0
        self.next_cue = 0
        self.judged = set()
        self.hits = 0
        self.finished = False
        self.success = False
        self.finish_time = 0

    def start(self, now):
        self.started_at = now + self.COUNTDOWN_MS
        self.next_cue = 0
        self.judged = set()
        self.hits = 0
        self.finished = False
        self.success = False
        self.finish_time = 0

    def target_time(self, index):
        return self.started_at + index * self.beat_ms

    def update(self, now, space_pressed):
        if self.finished:
            return

        while (
            self.next_cue < len(self.sequence)
            and now >= self.target_time(self.next_cue)
        ):
            self.tone_bank.play(self.sequence[self.next_cue])
            self.next_cue += 1

        if space_pressed:
            available = [
                index
                for index in range(self.next_cue)
                if index not in self.judged
                and 0 <= now - self.target_time(index) <= self.HIT_WINDOW_MS
            ]
            if available:
                index = available[-1]
                self.judged.add(index)
                self.hits += 1

        last_target = self.target_time(len(self.sequence) - 1)
        if now > last_target + self.HIT_WINDOW_MS:
            self.finished = True
            self.success = self.hits >= self.REQUIRED_HITS
            self.finish_time = now

    def draw(self, surface, fonts, now):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((18, 22, 30, 225))
        surface.blit(overlay, (0, 0))

        title = fonts["large"].render("MELODY TREE CONCERT", True, WHITE)
        surface.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        if self.finished:
            message = "GREAT! FOREST RESTORED" if self.success else "TRY AGAIN - SPACE"
            color = GOLD if self.success else (240, 140, 150)
            text = fonts["large"].render(message, True, color)
            surface.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            score = fonts["medium"].render(
                f"HITS {self.hits}/{len(self.sequence)}",
                True,
                WHITE,
            )
            surface.blit(score, score.get_rect(center=(WIDTH // 2, 400)))
            return

        if now < self.started_at:
            count = max(1, math.ceil((self.started_at - now) / 340))
            cue_text = str(count)
        else:
            cue_text = "SPACE!"

        cue = fonts["huge"].render(cue_text, True, GOLD)
        surface.blit(cue, cue.get_rect(center=(WIDTH // 2, 300)))

        beat_index = max(0, min(self.next_cue - 1, len(self.sequence) - 1))
        note = fonts["large"].render(self.sequence[beat_index], True, WHITE)
        surface.blit(note, note.get_rect(center=(WIDTH // 2, 390)))

        score = fonts["medium"].render(
            f"HITS {self.hits}/{len(self.sequence)}",
            True,
            WHITE,
        )
        surface.blit(score, score.get_rect(center=(WIDTH // 2, 465)))


class Game:
    """全員を持ち、各オブジェクトに仕事をお願いするゲーム監督。"""

    def __init__(self):
        self.audio_error = initialize_pygame()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixel Melody Quest")
        self.clock = pygame.time.Clock()
        self.fonts = {
            "small": pygame.font.Font(None, 26),
            "medium": pygame.font.Font(None, 38),
            "large": pygame.font.Font(None, 54),
            "huge": pygame.font.Font(None, 88),
        }
        self.tone_bank = ToneBank(enabled=self.audio_error is None)
        self.running = True
        self.reset()

    def reset(self):
        self.state = EXPLORE
        self.player = Player(WIDTH // 2 - 21, HEIGHT - 70)
        self.notes = make_note_spirits()
        self.monsters = [
            NoiseMonster(90, 300, 2),
            NoiseMonster(420, 335, -3),
            NoiseMonster(760, 275, 2),
            NoiseMonster(300, 500, -2),
        ]
        self.tree = MelodyTree()
        self.rhythm = RhythmChallenge(self.tone_bank)
        self.notice = "COLLECT 7 NOTE SPIRITS"
        self.notice_until = 0

    @property
    def collected_count(self):
        return sum(note.collected for note in self.notes)

    def process_events(self):
        space_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    space_pressed = True
                elif event.key == pygame.K_r and self.state == CLEAR:
                    self.reset()
        return space_pressed

    def collect_notes(self):
        note = collect_touching_note(self.player, self.notes, self.tone_bank)
        if note is not None:
            self.notice = f"{note.name}  {note.frequency:.1f} Hz"
            self.notice_until = pygame.time.get_ticks() + 1100

    def update_explore(self, now, space_pressed):
        self.player.update(pygame.key.get_pressed())
        self.collect_notes()

        for monster in self.monsters:
            monster.update()

        if handle_noise_hit(self.player, self.monsters, now):
            self.notice = "OUCH! NOTES ARE SAFE"
            self.notice_until = now + 1100

        self.tree.update(self.collected_count, len(self.notes))
        if self.tree.can_start(self.player):
            self.notice = "PRESS SPACE AT THE MELODY TREE"
            self.notice_until = now + 100
            if space_pressed:
                self.state = RHYTHM
                self.rhythm.start(now)

    def update_rhythm(self, now, space_pressed):
        if self.rhythm.finished and not self.rhythm.success and space_pressed:
            self.rhythm.start(now)
            return

        self.rhythm.update(now, space_pressed)
        if (
            self.rhythm.finished
            and self.rhythm.success
            and now >= self.rhythm.finish_time + 650
        ):
            self.state = CLEAR

    def update(self, now, space_pressed):
        # TODO 12: stateに合わせて、今必要な updateを呼ぼう。
        # EXPLOREなら self.update_explore(now, space_pressed)
        # RHYTHMなら self.update_rhythm(now, space_pressed)
        self.update_explore(now, space_pressed)

    def draw_forest(self):
        self.screen.fill((47, 55, 55))

        for index, note in enumerate(self.notes):
            restored = note.collected or self.state == CLEAR
            color = note.color if restored else (78, 86, 85)
            center_x = 70 + index * 135
            center_y = 205 + (index % 2) * 245
            pygame.draw.circle(self.screen, color, (center_x, center_y), 115)

        for x, y in [(35, 35), (150, 55), (785, 40), (875, 170), (40, 520)]:
            pygame.draw.rect(self.screen, (94, 72, 52), (x + 16, y + 28, 14, 45))
            pygame.draw.circle(self.screen, (68, 105, 80), (x + 23, y + 22), 28)

    def draw_hud(self, now):
        panel = pygame.Surface((WIDTH, 62), pygame.SRCALPHA)
        panel.fill((20, 25, 29, 210))
        self.screen.blit(panel, (0, HEIGHT - 62))

        for index in range(self.player.max_hearts):
            color = HEART if index < self.player.hearts else MIST
            x = 30 + index * 34
            pygame.draw.circle(self.screen, color, (x, HEIGHT - 34), 9)
            pygame.draw.circle(self.screen, color, (x + 13, HEIGHT - 34), 9)
            pygame.draw.polygon(
                self.screen,
                color,
                [
                    (x - 8, HEIGHT - 32),
                    (x + 21, HEIGHT - 32),
                    (x + 7, HEIGHT - 14),
                ],
            )

        note_text = self.fonts["medium"].render(
            f"NOTES {self.collected_count}/{len(self.notes)}",
            True,
            WHITE,
        )
        self.screen.blit(note_text, (150, HEIGHT - 49))

        if now <= self.notice_until or self.tree.can_start(self.player):
            notice = self.fonts["small"].render(self.notice, True, GOLD)
            self.screen.blit(notice, notice.get_rect(midright=(WIDTH - 24, HEIGHT - 31)))

        if self.audio_error:
            silent = self.fonts["small"].render("SILENT MODE", True, (245, 170, 120))
            self.screen.blit(silent, (WIDTH - 135, 14))

    def draw_clear(self, now):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((15, 24, 31, 115))
        self.screen.blit(overlay, (0, 0))

        for index in range(48):
            x = (index * 83 + now // 7) % WIDTH
            y = (index * 47 + now // 11) % HEIGHT
            color = NOTE_SPECS[index % len(NOTE_SPECS)][2]
            pygame.draw.rect(self.screen, color, (x, y, 8, 8))

        title = self.fonts["huge"].render("CLEAR!", True, GOLD)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 245)))
        message = self.fonts["large"].render("COLOR AND MUSIC ARE BACK", True, WHITE)
        self.screen.blit(message, message.get_rect(center=(WIDTH // 2, 335)))
        retry = self.fonts["medium"].render("PRESS R TO PLAY AGAIN", True, PAPER)
        self.screen.blit(retry, retry.get_rect(center=(WIDTH // 2, 405)))

    def draw(self, now):
        self.draw_forest()
        self.tree.draw(self.screen)

        for note in self.notes:
            note.draw(self.screen, now)
        for monster in self.monsters:
            monster.draw(self.screen)
        self.player.draw(self.screen, now)
        self.draw_hud(now)

        if self.state == RHYTHM:
            self.rhythm.draw(self.screen, self.fonts, now)
        elif self.state == CLEAR:
            self.draw_clear(now)

    def run(self):
        while self.running:
            now = pygame.time.get_ticks()
            space_pressed = self.process_events()
            self.update(now, space_pressed)
            self.draw(now)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    Game().run()
