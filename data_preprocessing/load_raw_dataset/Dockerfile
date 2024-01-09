FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_lrd.txt /pipeline
RUN pip install -r requirements_lrd.txt
COPY malicious_phish_copy.csv /pipeline
COPY load_raw_dataset.py /pipeline