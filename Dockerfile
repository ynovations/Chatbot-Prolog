FROM python:3.9-slim
LABEL authors="jpmantuano"

ADD requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["top", "-b"]