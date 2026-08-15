# Dev image: runs the Vite dev server with hot-reload. For production you would
# build the static bundle and serve it behind nginx instead.
FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
