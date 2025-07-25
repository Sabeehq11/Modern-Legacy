FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/

# Create directories for static and media files
RUN mkdir -p /var/www/lms/static /var/www/lms/media \
             /var/www/cms/static /var/www/cms/media

# Set permissions
RUN chown -R nginx:nginx /var/www/

# Expose ports
EXPOSE 80 443

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
