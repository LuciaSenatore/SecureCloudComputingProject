FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_uhe.txt /pipeline
RUN pip install -r requirements_uhe.txt
COPY url_https_ext.py /pipeline