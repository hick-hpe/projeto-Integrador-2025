# =========================
# Stage 1: Build / Development
# =========================
FROM node:latest AS build

# Diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar o restante do código
COPY . .

# Expor porta do Vite (React dev server)
EXPOSE 5173

# Comando para desenvolvimento
CMD ["npm", "run", "dev", "--", "--host"]

# =========================
# Stage 2: Production
# =========================
# FROM nginx:stable-alpine AS production

# # Copiar build do React para Nginx
# COPY --from=build /app/dist/ /usr/share/nginx/html

# # Substituir configuração padrão do Nginx, se houver
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# # Expor porta HTTP
# EXPOSE 80

# # Comando para rodar Nginx em foreground
# CMD ["nginx", "-g", "daemon off;"]