FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements_ucle.txt /pipeline
RUN pip install -r requirements_ucle.txt
COPY url_count_letters_ext.py /pipeline