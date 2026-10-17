"""CLI-интерфейс для генератора."""
import argparse
import sys
from pathlib import Path

from .generator import OutroGenerator
from .models import OutroConfig
from .utils import validate_hex_color


def parse_args() -> OutroConfig:
    parser = argparse.ArgumentParser(
        description="Генератор динамического YouTube-аутро",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Пример:
  python -m src.cli --name "Мой Канал" --color "#FF3366" --cta "Подпишись!"
        """
    )
    parser.add_argument("--name", required=True, help="Название канала")
    parser.add_argument("--color", required=True,
                        help="Цвет акцента в HEX (#RRGGBB)")
    parser.add_argument("--cta", required=True,
                        help="Текст призыва (например, 'Подпишись')")
    parser.add_argument("--duration", type=float, default=5.0,
                        help="Длительность видео в секундах (по умолчанию 5)")

    args = parser.parse_args()

    # Валидация цвета
    try:
        validate_hex_color(args.color)
    except ValueError as e:
        parser.error(str(e))

    return OutroConfig(
        channel_name=args.name,
        accent_hex=args.color,
        cta_text=args.cta,
        duration=args.duration,
    )


def main():
    try:
        config = parse_args()
        print(f"🎬 Генерирую аутро для канала '{config.channel_name}'...")
        gen = OutroGenerator(config)
        out_path = gen.generate()
        print(f"✅ Готово! Файл сохранён: {out_path}")
    except (ValueError, FileNotFoundError) as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()