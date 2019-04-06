FROM python:3.7-alpine

WORKDIR /root

RUN apk add --no-cache \
    dumb-init
RUN pip install --no-cache-dir \
    flask

ENV FLASK_APP="app.py"
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/usr/local/bin/python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80

COPY . .
