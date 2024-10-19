FROM python:3.12
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
ADD . /app/src/app
COPY manage.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt