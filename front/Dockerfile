FROM nginx:alpine

# Copiar archivos HTML y recursos estáticos
COPY *.html /usr/share/nginx/html/
COPY *.png /usr/share/nginx/html/
COPY *.jpeg /usr/share/nginx/html/
COPY *.jpg /usr/share/nginx/html/

# Copiar componentes JavaScript reutilizables
COPY components/ /usr/share/nginx/html/components/

# Copiar documentación
COPY *.md /usr/share/nginx/html/docs/

# Copiar configuración personalizada de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto 80
EXPOSE 80

# Comando por defecto (nginx lo inicia automáticamente)
CMD ["nginx", "-g", "daemon off;"]
