FROM node:14-alpine
WORKDIR /app
COPY ./src .
RUN apk update && \
    apk add --no-cache git && \
    npm install && \
    apk del git
ENTRYPOINT ["npm"]
CMD ["run", "prod"]
