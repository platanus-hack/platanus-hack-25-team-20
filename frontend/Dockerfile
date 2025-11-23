FROM node:25-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Set API URL to use nginx proxy (empty means relative URLs)
ENV VITE_API_URL=""

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Set default backend URL for docker-compose compatibility
ENV BACKEND_URL=http://backend:8000

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
