FROM python:3.9.10

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./

CMD ["python", "-u", "app.py"]