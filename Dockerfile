FROM python:3.7 as build-py

## Backend
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt

FROM python:3.7-slim as final-image

RUN groupadd -r acdc && useradd -r -g acdc acdc

RUN mkdir /app

COPY . /app
COPY --from=build-py /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=build-py /usr/local/bin/ /usr/local/bin/

WORKDIR /app

RUN mkdir -p static media

CMD ./acdcstart.sh
