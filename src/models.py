"""Data-классы для параметров генерации."""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OutroConfig:
    """Конфигурация одного аутро."""
    channel_name: str
    accent_hex: str
    cta_text: str
    width: int = 1920
    height: int = 1080
    duration: float = 5.0
    fps: int = 30
    output_path: str = ""

    @property
    def accent_rgb(self) -> Tuple[int, int, int]:
        from .utils import validate_hex_color
        return validate_hex_color(self.accent_hex)