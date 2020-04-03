FROM python:3.8.2-slim

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apt-get update && apt-get install -y ca-certificates firefox-esr tzdata wget && rm -rf /var/lib/apt/lists/* \
    && cd /tmp \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz \
    && tar xvfz geckodriver-v0.23.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin \
    && rm geckodriver-v0.23.0-linux64.tar.gz \
    && pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY *.py ./

ENV TZ="Europe/Berlin" \
    URL="https://this.de" \
    PICTUREPATH="/usr/local" \
    TELEGRAMBOTKEY="bot4711" \
    CHATID=4711 \
    XPATH="bot4711" \
    STATUSTEXT="Derzeit online nicht lieferbar"

CMD ["python3", "checker.py"]