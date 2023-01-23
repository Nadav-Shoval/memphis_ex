FROM python:3.9.9-slim-buster AS python
COPY consumer consumer
RUN pip install -r consumer/requirements.txt

FROM python AS base
COPY common /consumer/common
RUN pip install -r /consumer/common/requirements.txt

FROM base AS src

WORKDIR consumer
CMD ["python3", "-t", "main.py"]