FROM python:3.11.9

RUN mkdir tgbot_serviceChecker

WORKDIR /tgbot_serviceChecker

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade head

CMD python app/main.py