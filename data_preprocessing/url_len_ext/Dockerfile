FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_ule.txt /pipeline
RUN pip install -r requirements_ule.txt
COPY url_len_ext.py /pipeline