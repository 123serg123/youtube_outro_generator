"""Утилиты: валидация, цвета, пути. Windows-friendly."""
import re
from pathlib import Path
from typing import Tuple

# Базовая директория проекта (независимо от OS)
BASE_DIR = Path(__file__).resolve().parent.parent
FONTS_DIR = BASE_DIR / "fonts"
OUTPUT_DIR = BASE_DIR / "output"


def validate_hex_color(color: str) -> Tuple[int, int, int]:
    """Конвертирует HEX в RGB. Поддерживает #RRGGBB и RRGGBB."""
    color = color.strip().lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", color):
        raise ValueError(f"Некорректный HEX-цвет: '{color}'. Ожидается формат #RRGGBB")
    return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))


def ensure_dir(path: Path) -> Path:
    """Создаёт директорию, если её нет."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(name: str) -> str:
    """Превращает имя канала в безопасное имя файла."""
    # Убираем всё, кроме букв, цифр, пробелов и дефисов
    clean = re.sub(r"[^\w\s\-а-яА-ЯёЁ]", "", name).strip()
    return clean.replace(" ", "_") or "channel"