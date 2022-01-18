FROM ubuntu:20.04

RUN apt update
RUN apt install -y python3 python3-pip nginx

COPY backend/nginx/ dest

COPY ./backend /backend

RUN chmod +x /backend/start.sh

WORKDIR /backend

RUN pip install -r requirements.txt

CMD [ "/backend/start.sh" ] 