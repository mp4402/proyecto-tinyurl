FROM python:3-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app/
COPY . .

CMD ["python", "app.py"]