FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_dt.txt /pipeline
RUN pip install -r requirements_dt.txt
COPY decision_tree.py /pipeline