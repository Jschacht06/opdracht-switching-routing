FROM nodered/node-red:latest

USER root

COPY node-red-data/package*.json /usr/src/node-red/

WORKDIR /usr/src/node-red
RUN npm install --omit=dev

USER node-red