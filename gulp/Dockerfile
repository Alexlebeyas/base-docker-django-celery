FROM node:boron-alpine

ADD package.json /PROJECT_NAME/gulp/package.json
WORKDIR /PROJECT_NAME/gulp/

RUN npm install -g gulp-cli && npm install
