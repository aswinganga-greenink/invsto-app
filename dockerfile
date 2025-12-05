FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .

# Libatomic, openssl for prisma - it isnt covered in slim model
RUN apt-get update && apt-get install -y \
    curl \
    libatomic1 \
    openssl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt


COPY . .

RUN python3 -m prisma generate

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]