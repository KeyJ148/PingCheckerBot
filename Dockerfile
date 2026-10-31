FROM python:3.14.9-alpine3.24

EXPOSE 8080
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk add iputils
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

CMD [ "python", "-u", "./ping_checker_bot.py" ]