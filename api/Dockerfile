FROM python:3.9.10

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py

CMD ["python", "-u", "main.py"]