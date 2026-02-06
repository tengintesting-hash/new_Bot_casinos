# Telegram Web App Casino Ecosystem

Повний стек для Telegram WebApp казино з FastAPI, aiogram та React.

## Структура
- `backend/` — FastAPI API та адмінка.
- `bot/` — Telegram бот на aiogram.
- `frontend/` — React WebApp.
- `nginx/` — конфігурація проксі.

## Швидкий старт

1. Скопіюйте `.env.example` у `.env` та заповніть змінні.
2. Запустіть сервіси:

```bash
docker compose up --build
```

## Основні ендпоїнти
- `/api/auth` — авторизація через `initData`.
- `/api/offers` — список активних пропозицій.
- `/admin/*` — адмінські маршрути (з `X-Admin-Token`).
- `/postback` — постбек трекера.

## Примітки
- SQLite база розміщується у томі `db_volume`.
- Nginx проксить `/api`, `/admin`, `/postback` на бекенд.
- Всі повідомлення UI та бота — українською.
