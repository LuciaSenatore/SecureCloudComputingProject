FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_use.txt /pipeline
RUN pip install -r requirements_use.txt
COPY url_shortserv_ext.py /pipeline