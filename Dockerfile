FROM python:3.10

WORKDIR /web
COPY . /web/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /web/

VOLUME /web/
EXPOSE 5000

CMD python3 main.py
