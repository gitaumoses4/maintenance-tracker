FROM node:20.10.0-alpine3.10
WORKDIR /usr/app/

COPY . /usr/app

RUN yarn install

EXPOSE 3003

CMD ["yarn", "start"]
