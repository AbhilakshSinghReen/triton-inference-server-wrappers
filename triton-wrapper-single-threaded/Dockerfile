FROM python:3.11-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y ffmpeg
RUN apt-get install -y libsm6
RUN apt-get install -y libxext6

COPY requirements.txt .

# RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt
# TODO:AbhilakshSinghReen the above pip install should not fail, the following command is a temporary solution
RUN cat requirements.txt | xargs -n 1 pip install --no-cache-dir --default-timeout=100

COPY . .

EXPOSE 7004

CMD ["gunicorn", "--workers", "1", "--threads", "1", "--timeout", "120", "--bind", "0.0.0.0:7004", "src.app:app"]
