FROM node:24-alpine

WORKDIR /app

COPY package.json package-lock.json ./
# Install all dependencies including devDependencies (tsx)
RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npx", "tsx", "src/server.ts"]
