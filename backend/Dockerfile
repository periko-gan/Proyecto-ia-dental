FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1

WORKDIR /app/backend

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		libgl1 \
		libglib2.0-0 \
		libgomp1 \
	&& rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
	&& pip install -r requirements.txt

COPY backend/ ./
COPY ["entrenamiento ia/runs/train/dental_definitivo_optimizado_medium/weights/best.pt", "/app/entrenamiento ia/runs/train/dental_definitivo_optimizado_medium/weights/best.pt"]

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

