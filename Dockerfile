FROM python:3-alpine

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . .

CMD ["python", "app.py"]