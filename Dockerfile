FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y gcc python3-dev libsasl2-dev libffi-dev libpq-dev git && rm -rf /var/lib/apt/lists/*
WORKDIR /src/nacmis
COPY requirements.txt /src/nacmis
RUN pip install --no-cache-dir -r requirements.txt
COPY . /src/nacmis/
ENV PYTHONPATH="/:$PYTHONPATH"
ENV DJANGO_SETTINGS_MODULE=nacmis_online.settings

EXPOSE 8000
CMD ["gunicorn", "nacmis_online.wsgi"]

