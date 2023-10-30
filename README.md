## Установка зависимостей

```sh
(venv)...$ pip install fastapi "uvicorn[standard]" python-multipart
```
**standard** - помимо wsgi сервера будут установлены python-dotenv, watchdog 
(перезапускает сервер при изменениях в коде)
**python-multipart** - для загрузки файлов

### Запуск сервера

```sh
(venv)...$ uvicorn main:app --reload
```

### Доступ к автоматически сгенерированной документации
```sh
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/docs
```
1) **Redoc** - не позволяет выполнять запросы интерактивно
2) **Swagger** - позволяет выполнять запросы