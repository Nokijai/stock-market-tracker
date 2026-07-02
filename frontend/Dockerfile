# ─────────────────────────────────────────────
# Stage 1: Build the React/Vite application
# ─────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package manifests first for layer-cache efficiency
COPY package.json package-lock.json* ./

# Clean install — uses exact versions from package-lock.json
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# ─────────────────────────────────────────────
# Stage 2: Serve with nginx on port 3000
# ─────────────────────────────────────────────
FROM nginx:alpine AS final

# Remove the default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Write a custom nginx config inline (no heredoc — RUN printf is portable)
RUN printf 'server {\n\
    listen 3000;\n\
    server_name _;\n\
\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
\n\
    # SPA fallback — serve index.html for all unmatched routes\n\
    location / {\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
\n\
    # Gzip compression\n\
    gzip on;\n\
    gzip_types text/plain text/css application/json application/javascript\n\
               text/xml application/xml application/xml+rss text/javascript;\n\
    gzip_min_length 256;\n\
}\n' > /etc/nginx/conf.d/app.conf

# Copy the built static assets from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
