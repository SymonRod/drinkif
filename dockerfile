FROM python:latest

RUN pip install django

COPY ./backend /backend
WORKDIR /backend

CMD [ "/backend/start.sh" ] 