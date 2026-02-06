# Telegram Web App Casino Ecosystem

Повний стек для Telegram WebApp казино з FastAPI, aiogram та React.

## Структура
- `backend/` — FastAPI API та адмінка.
- `bot/` — Telegram бот на aiogram.
- `frontend/` — React WebApp.
- `nginx/` — конфігурація проксі.

## Швидкий старт

1. Скопіюйте `.env.example` у `.env` та заповніть змінні (WEBAPP_URL має бути HTTPS; для blacktime.uno використовуйте `https://blacktime.uno:8443`).
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

## Усунення проблем
- Якщо бот все ще показує попередження про `parse_mode`, переконайтесь що образ перезібраний: `docker compose build --no-cache bot` або `docker compose up --build --force-recreate`.
- `WEBAPP_URL` має бути HTTPS, інакше Telegram не дозволить кнопку WebApp.
- Якщо WebApp не відкривається через домен, перевірте DNS, відкриті порти 8080/8443 та налаштуйте HTTPS. У `nginx/ssl.conf.example` є шаблон для SSL (certbot/letsencrypt).
