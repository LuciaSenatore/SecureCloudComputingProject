FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_ucde.txt /pipeline
RUN pip install -r requirements_ucde.txt
COPY url_count_digit_ext.py /pipeline