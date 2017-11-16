FROM ubuntu:16.04

EXPOSE 80

CMD ["python3", "main.py"]

RUN apt-get update && xargs apt-get install -y python3-dev && xargs apt-get install -y python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY deps/python-main.txt /

RUN pip3 install --disable-pip-version-check -r python-main.txt

COPY /main.py /
