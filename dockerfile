FROM ubuntu:20.04

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update
RUN apt install -y python3 python3-pip nginx libpq-dev

COPY backend/nginx /etc/nginx/sites-enabled
COPY backend/drinkif/static /var/www/html


COPY ./backend /backend

RUN chmod +x /backend/start.sh

WORKDIR /backend

CMD [ "/backend/start.sh" ] 