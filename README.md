## Запуск проекта ✨
___

### Скачайте проект  

```shell
    git clone https://github.com/BlaackWizard/hackaton.git
    cd hackaton
```


### Установите зависимости

```shell
    python3 -m venv .venv
    source .venv/bin/activate # Для MacOS/Linux
    source .venv/Scripts/activate # Для Windows
    pip install -r requirements.txt
```

### Проставьте необходимые данные
Зайдите в директорию backends и создайте файл .env.

После подставляете значения из файла .env.example

```text
    POSTGRES_USERNAME=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_DATABASE=db
    
    API_TOKEN=... (ваш апи токен ии)
    BASE_URL=... (ваша ссылка на ии)
```

### Миграция бд

```shell
  make migrations
  make upgrade-migrations
```

### Запустите файл fast_api.py
Файл находится по адресу backend/src/bootstrap/entrypoint/fast_api.py


### [Архитектура приложения](docs/arch.md)
