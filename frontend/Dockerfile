FROM node:18-alpine

WORKDIR /nextjs

COPY package.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
