"""Основной генератор YouTube-аутро."""
import random
from pathlib import Path
from typing import List

import numpy as np
from moviepy.editor import (
    ColorClip, ImageClip, CompositeVideoClip,
    concatenate_videoclips
)

from .effects import (
    Particle, make_gradient_frame, render_text_frame
)
from .models import OutroConfig
from .utils import FONTS_DIR, OUTPUT_DIR, ensure_dir, safe_filename


class OutroGenerator:
    """Генерирует 5-секундное YouTube-аутро с анимацией."""

    FONT_FILE = FONTS_DIR / "Montserrat-Bold.ttf"

    def __init__(self, config: OutroConfig):
        self.config = config
        self._validate()
        # Детерминированный рандом — одинаковые частицы при повторном запуске
        self.rng = random.Random(hash(config.channel_name) & 0xFFFFFFFF)

    def _validate(self):
        if not self.config.channel_name.strip():
            raise ValueError("Имя канала не может быть пустым")
        if not self.config.cta_text.strip():
            raise ValueError("CTA-текст не может быть пустым")
        if not self.FONT_FILE.exists():
            raise FileNotFoundError(
                f"Шрифт не найден: {self.FONT_FILE}. "
                "Скачай Montserrat-Bold.ttf и положи в папку fonts/"
            )

    def _init_particles(self, count: int = 60) -> List[Particle]:
        accent = self.config.accent_rgb
        # Светлая версия акцента для частиц
        light_accent = tuple(min(255, c + 60) for c in accent)
        return [
            Particle(self.config.width, self.config.height, light_accent, self.rng)
            for _ in range(count)
        ]

    def _render_frame(self, t: float, particles: List[Particle],
                      bg_frame: np.ndarray) -> np.ndarray:
        """Рендерит один кадр в момент времени t (секунды)."""
        from PIL import Image
        cfg = self.config
        progress = min(t / 1.5, 1.0)  # текст появляется за 1.5 сек

        # Фон + частицы
        bg_img = Image.fromarray(bg_frame).convert("RGBA")
        from PIL import ImageDraw
        draw = ImageDraw.Draw(bg_img)
        for p in particles:
            p.update()
            p.draw(draw)

        # Текст поверх
        text_layer = render_text_frame(
            cfg.width, cfg.height,
            cfg.channel_name, cfg.cta_text,
            cfg.accent_rgb, progress,
            self.FONT_FILE
        )
        text_img = Image.fromarray(text_layer)

        # Композит
        composed = Image.alpha_composite(bg_img, text_img)
        return np.array(composed.convert("RGB"))

    def generate(self) -> Path:
        """Генерирует видео и возвращает путь к нему."""
        cfg = self.config
        ensure_dir(OUTPUT_DIR)

        # Фоновый градиент (тёмный → акцентный)
        bg_frame = make_gradient_frame(
            cfg.width, cfg.height,
            color_top=(15, 15, 25),
            color_bottom=tuple(c // 3 for c in cfg.accent_rgb)
        )

        particles = self._init_particles()

        # Собираем клип через make_frame
        def make_frame(t):
            return self._render_frame(t, particles, bg_frame)

        from moviepy.editor import VideoClip
        clip = VideoClip(make_frame, duration=cfg.duration)
        clip = clip.set_fps(cfg.fps).set_audio(None)

        # Имя файла
        safe_name = safe_filename(cfg.channel_name)
        out_path = OUTPUT_DIR / f"youtube_outro_{safe_name}.mp4"

        try:
            clip.write_videofile(
                str(out_path),
                codec="libx264",
                audio=False,
                preset="medium",
                bitrate="5000k",
                logger=None  # тишина в консоли
            )
        except Exception as e:
            raise RuntimeError(f"Ошибка рендера видео: {e}") from e
        finally:
            clip.close()

        return out_path

