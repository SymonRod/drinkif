FROM python:latest

RUN pip install django
RUN pip install psycopg2

COPY ./backend /backend

RUN chmod +x /backend/start.sh

WORKDIR /backend

RUN pip3 install -r requirements.txt

CMD [ "/backend/start.sh" ] 