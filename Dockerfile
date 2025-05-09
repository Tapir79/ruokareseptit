FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y sqlite3 coreutils && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN chmod +x /app/install.sh

RUN pip install --no-cache-dir flask

ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD /bin/sh -c '\
  if [ ! -f /app/database.db ]; then \
      echo "database.db missing – running install.sh"; \
      yes | /app/install.sh; \
  else \
      echo "Using existing /app/database.db"; \
  fi && \
  exec flask run --host 0.0.0.0'
