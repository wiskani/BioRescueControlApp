FROM node:18-alpine

WORKDIR /nextjs

COPY package.json ./

RUN npm install 

COPY . .

RUN npm run build

COPY --from=builder /app/public ./public

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
