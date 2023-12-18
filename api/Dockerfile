FROM python:3.10.12-slim-buster
WORKDIR /usr/app

RUN apt update
RUN apt install -y libpq-dev gcc

# Install dependencies
COPY requirements.txt /usr/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code
COPY . /usr/app/

CMD ["/bin/sh", "-c", "/usr/app/entrypoint.sh"]
