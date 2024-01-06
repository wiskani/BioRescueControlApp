FROM node:18-alpine

WORKDIR /nextjs

COPY package.json ./

RUN npm build 

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
