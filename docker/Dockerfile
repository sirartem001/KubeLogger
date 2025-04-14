FROM python:3.9-slim

WORKDIR /app
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

COPY ./app .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]