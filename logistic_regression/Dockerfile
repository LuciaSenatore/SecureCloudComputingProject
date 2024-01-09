FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_lr.txt /pipeline
RUN pip install -r requirements_lr.txt
COPY logistic_regression.py /pipeline