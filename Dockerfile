FROM python:3.9-slim-buster
RUN mkdir /app \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y wget \
    && apt-get install -y git

WORKDIR /app
COPY requirements.txt /app
COPY get_block.py /app
COPY new_block.py /app
COPY dbdocker.py /app
RUN pip install -r requirements.txt
EXPOSE 6060
CMD [ "python", "-u", "new_block.py" ]
