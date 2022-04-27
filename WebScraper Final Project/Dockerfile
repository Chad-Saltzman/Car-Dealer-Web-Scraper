FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

RUN ["python3", "./WebScraperUnitTest.py"]

CMD ["python3", "./WebScraperIntegrationTest.py"]
