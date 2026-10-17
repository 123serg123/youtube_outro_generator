# YouTube Outro Generator

Консольный генератор динамического аутро для YouTube: процедурный градиент,
«летящие» частицы в цвете канала, имя и призыв с поддержкой кириллицы.
На выходе — готовый mp4 (1920×1080, 30 fps, H.264).

## Характеристики

| Параметр | Значение |
|---|---|
| Разрешение | 1920×1080 (Full HD) |
| FPS | 30 |
| Длительность | 5 сек (настраивается `--duration`) |
| Кодек | H.264 (libx264), без звука |
| Текст | TTF с кириллицей (Montserrat Bold) |

## Возможности

- CLI с валидацией аргументов (HEX-цвет, обязательные поля)
- Процедурная анимация градиента и частиц без готовых ассетов
- Офлайн-установка зависимостей из локального кэша `packages/`
  (`pip --no-index --find-links`) — воспроизводимо без сети
- Чистая архитектура: `models` (конфиг) · `generator` (рендер) ·
  `effects` (анимация) · `utils` (хелперы) · `cli` (точка входа)

## Быстрый старт

### 1. Требования
- Windows 10/11, Python 3.12
- Шрифт: скачайте
  [Montserrat-Bold.ttf](https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Bold.ttf)
  и положите в `fonts/`

### 2. Установка зависимостей (офлайн, из кэша `packages/`)
```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install --no-index --find-links=packages moviepy
```

### 3. Генерация
```powershell
$env:PYTHONUTF8 = "1"
.\venv\Scripts\python.exe -m src.cli --name "Мой Канал" --color "#FF3366" --cta "Подпишись!"
```
Результат: `output/youtube_outro_Мой_Канал.mp4`

## Аргументы CLI

| Аргумент | Обязательный | Описание |
|---|---|---|
| `--name` | да | Название канала |
| `--color` | да | Акцентный цвет, HEX `#RRGGBB` |
| `--cta` | да | Текст призыва к действию |
| `--duration` | нет | Длительность в секундах (по умолчанию 5) |

## Структура проекта

```
youtube_outro_generator/
├── src/
│   ├── cli.py        # точка входа: разбор и валидация аргументов
│   ├── models.py     # OutroConfig — конфигурация рендера
│   ├── generator.py  # OutroGenerator — сборка сцены и экспорт mp4
│   ├── effects.py    # анимации градиента и частиц
│   └── utils.py      # пути, валидация HEX, безопасные имена файлов
├── fonts/            # TTF-шрифт (вне репозитория)
├── output/           # готовые mp4 (вне репозитория)
├── packages/         # офлайн-кэш wheel (вне репозитория)
└── requirements.txt
```

## Стек

Python 3.12 · moviepy 1.0.3 · Pillow 11.1 · NumPy · imageio-ffmpeg

## Лицензии

Код проекта — MIT. Шрифт Montserrat — SIL Open Font License 1.1.