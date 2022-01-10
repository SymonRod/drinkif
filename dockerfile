FROM python:latest

RUN pip install django
RUN pip install psycopg2

COPY ./backend /backend

RUN chmod +x /backend/start.sh

WORKDIR /backend

CMD [ "/backend/start.sh" ] 