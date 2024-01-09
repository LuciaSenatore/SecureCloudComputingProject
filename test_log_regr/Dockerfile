FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_tlr.txt /pipeline
RUN pip install -r requirements_tlr.txt
COPY test_logistic_regression.py /pipeline