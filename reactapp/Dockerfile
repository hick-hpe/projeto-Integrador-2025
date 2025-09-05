# Usar uma imagem base do Node.js
FROM node:latest

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os ficheiros do projeto para o container
COPY package*.json ./

# Instalar as dependências do projeto
RUN npm install

# Copiar o resto do código da aplicação
COPY . .

# Expor a porta que o servidor de desenvolvimento do React usa
EXPOSE 5173

# Comando para iniciar o servidor de desenvolvimento
CMD ["npm", "run", "dev", "--", "--host"]

# Production Stage
# RUN rm -rf /usr/share/nginx/html/*

# FROM nginx:stable-alpine AS production

# COPY --from=build /app/dist/ /usr/share/nginx/html

# # Copia o arquivo nginx.conf para substituir o padrão
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]


