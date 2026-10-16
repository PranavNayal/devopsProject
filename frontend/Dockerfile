# Stage 1: Build React static assets
FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve with unprivileged NGINX (Non-Root User: UID 101)
FROM nginxinc/nginx-unprivileged:1.27-alpine

# Copy built frontend assets
COPY --from=build /app/dist /usr/share/nginx/html

# Copy reverse proxy server block
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Unprivileged NGINX runs on port 8080 by default as non-root user 'nginx' (UID 101)
USER 101

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
