FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN npm install

COPY . .
RUN npm run build

# Etapa 2: imagem final, usando Nginx para servir os arquivos estáticos
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Remove o arquivo de configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Adiciona um arquivo de configuração customizado para React SPA
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]