FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_tdt.txt /pipeline
RUN pip install -r requirements_tdt.txt
COPY test_decision_tree.py /pipeline