FROM python:3.6-alpine

RUN apk --update add --no-cache g++

RUN pip install numpy

COPY *.py /

ENTRYPOINT ["python", "SAT.py"]
