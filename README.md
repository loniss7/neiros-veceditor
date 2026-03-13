# Vector Editor CLI

Тестовое задание Neiros: векторный редактор с интерфейсом командной строки.

## Что реализовано

- создание фигур: `Point`, `Segment`, `Circle`, `Square`
- сохранение во временной памяти текущей сессии
- удаление фигур по `id`
- просмотр списка фигур
- валидация входных данных
- menu-driven CLI на `questionary`
- стилизованный вывод на `rich`
- архитектура с разделением на `domain / services / repositories / cli`
- unit-тесты на `pytest` для domain, repository, service и CLI слоёв
- хранение фигур в локальной SQLite-базе между запусками приложения

## Support

- Python 3.13

## Update

- Добавлены новые фигуры: `Oval`, `Rectangle`
