FROM node:8-alpine

RUN apk update && \
    apk add make ruby ruby-dev glib-dev build-base && \
    rm -rf /var/cache/apk/*

WORKDIR /app
ADD . .
EXPOSE 7777

RUN make install

CMD ["make", "run"]
