# build stage
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
RUN npm install luxon
COPY . .
RUN npm run build


# production stage: serve static with nginx
FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
# default nginx config is sufficient; ensure container listens on 80
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
