FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_sr.txt /pipeline
RUN pip install -r requirements_sr.txt
COPY show_result.py /pipeline