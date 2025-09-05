# Build Stag
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json* ./

RUN npm install

COPY . .

# RUN npm run build

# EXPOSE 5173

# Development
# CMD ["npm", "run", "dev", "--", "--host"]

# Production Stage
# RUN rm -rf /usr/share/nginx/html/*

# FROM nginx:stable-alpine AS production

# COPY --from=build /app/dist/ /usr/share/nginx/html

# # Copia o arquivo nginx.conf para substituir o padrão
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
