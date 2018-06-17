FROM node:latest
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/images
WORKDIR /usr/src/app
COPY package.json package-lock.json /usr/src/app/
RUN npm install
COPY . /usr/src/app

CMD ["node", "index.js"]