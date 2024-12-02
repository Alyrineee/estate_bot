FROM python

WORKDIR /app

COPY requirements/prod.txt .

RUN pip install --no-cache-dir -r prod.txt

COPY . .

CMD ["python", "run.py"]

