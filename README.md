># Trade.AI
>Automated algorithmic trading bot using python

## Project Requirements
>- Git
>- Docker
>- Python 3.8+
>- Django
>- Django Rest Framework
>- PostgresDB
>- Redis
>- Celery

## Project Setup Guide
> 1. Install [Git](https://git-scm.com/downloads), [Docker](https://www.docker.com/).
> 2. Clone [Trade.AI](https://github.com/aditya-verma/trade_ai.git) repository.
> 3. Create .env file to store the following environment variables.
>   > TRADEAI_DB_NAME=<TRADEAI_DB_NAME> </br>
      TRADEAI_DB_USER_NAME=<TRADEAI_DB_USER_NAME> </br>
      TRADEAI_DB_USER_PASSWORD=<TRADEAI_DB_USER_PASSWORD> </br>
      TRADEAI_DB_HOST=<TRADEAI_DB_HOST> </br>
      TRADEAI_DB_PORT=<TRADEAI_DB_PORT> </br>
      TRADEAI_TEST=<TRUE_OR_FALSE> </br>
      BINANCE_API_KEY=<BINANCE_API_KEY> </br>
      BINANCE_API_SECRET=<BINANCE_API_SECRET> </br>
      TELEGRAM_BOT_TOKEN=<TELEGRAM_BOT_TOKEN> 
> 4. Run ```docker-compose up -d``` to build the docker container and deploy the project inside the container. 
