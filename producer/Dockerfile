FROM python:3.9.9-slim-buster AS python
COPY producer producer
RUN pip install -r producer/requirements.txt

FROM python AS base
COPY common /producer/common
RUN pip install -r /producer/common/requirements.txt

FROM base AS src

WORKDIR producer
CMD ["python3", "-t", "main.py"]