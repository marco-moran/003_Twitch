FROM python:3.8-buster
RUN apt-get update
WORKDIR /usr/app
RUN python -m pip install --upgrade pip
COPY requirements.txt /usr/app/
COPY analisi.py /usr/app/
RUN pip install -r requirements.txt
RUN rm requirements.txt
CMD python analisi.py
