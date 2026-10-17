"""Визуальные эффекты: градиент, частицы, анимация текста."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import List
import random


class Particle:
    """Простая частица для фонового эффекта."""
    def __init__(self, width: int, height: int, color: tuple, rng: random.Random):
        self.x = rng.uniform(0, width)
        self.y = rng.uniform(0, height)
        self.size = rng.uniform(2, 6)
        self.vx = rng.uniform(-0.8, 0.8)
        self.vy = rng.uniform(-1.5, -0.3)  # движутся вверх
        self.alpha = rng.uniform(0.3, 0.9)
        self.color = color
        self.width = width
        self.height = height

    def update(self):
        self.x += self.vx
        self.y += self.vy
        # Респавн снизу, если ушла за верх
        if self.y < -10:
            self.y = self.height + 10
            self.x = random.uniform(0, self.width)

    def draw(self, draw_ctx: ImageDraw.ImageDraw):
        rgba = self.color + (int(self.alpha * 255),)
        draw_ctx.ellipse(
            [self.x - self.size, self.y - self.size,
             self.x + self.size, self.y + self.size],
            fill=rgba
        )


def make_gradient_frame(width: int, height: int,
                        color_top: tuple, color_bottom: tuple) -> np.ndarray:
    """Вертикальный градиент как numpy-массив (RGB)."""
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    for c in range(3):
        col = np.linspace(color_top[c], color_bottom[c], height, dtype=np.uint8)
        arr[:, :, c] = col[:, None]
    return arr


def ease_out_cubic(t: float) -> float:
    """Плавное замедление для анимации."""
    return 1 - (1 - t) ** 3


def render_text_frame(width: int, height: int,
                        channel_name: str, cta_text: str,
                        accent_rgb: tuple, progress: float,
                        font_path: Path) -> np.ndarray:
    """
    Рендерит кадр с текстом.
    progress: 0..1 — прогресс анимации появления.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Шрифты
    try:
        font_title = ImageFont.truetype(str(font_path), 120)
        font_cta = ImageFont.truetype(str(font_path), 60)
    except OSError:
        # Fallback на системный, если шрифт не найден
        font_title = ImageFont.load_default()
        font_cta = ImageFont.load_default()

    # Анимация: появление снизу с замедлением + fade
    eased = ease_out_cubic(min(progress * 1.5, 1.0))
    alpha = int(min(progress * 2, 1.0) * 255)
    offset_y = int((1 - eased) * 80)

    # Название канала (по центру)
    title_bbox = draw.textbbox((0, 0), channel_name, font=font_title)
    tw, th = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
    tx = (width - tw) // 2
    ty = (height - th) // 2 - 60 + offset_y
    draw.text((tx, ty), channel_name, font=font_title,
              fill=accent_rgb + (alpha,))

    # CTA-текст ниже
    cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
    cw, ch = cta_bbox[2] - cta_bbox[0], cta_bbox[3] - cta_bbox[1]
    cx = (width - cw) // 2
    cy = ty + th + 40 + offset_y
    # CTA появляется с небольшой задержкой
    cta_progress = max(0, (progress - 0.2) / 0.8)
    cta_alpha = int(min(cta_progress * 2, 1.0) * 255)
    draw.text((cx, cy), cta_text, font=font_cta,
              fill=(255, 255, 255, cta_alpha))

    return np.array(img)