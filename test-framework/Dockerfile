FROM python:3.9-alpine

WORKDIR /tests

RUN apk add --no-cache gcc musl-dev

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .

CMD ["sh", "-c", "sleep 5 && pytest -v -n 3 --alluredir=/tests/allure-results"]

