# Use the official NGINX image as the base image
FROM nginx:latest

# Copy your custom NGINX configuration file
COPY ./default.conf /etc/nginx/conf.d/default.conf

# Copy your HTML, CSS, and JavaScript files into the NGINX web root directory
COPY ./index.html /usr/share/nginx/html/
COPY ./style.css /usr/share/nginx/html/
COPY ./code.js /usr/share/nginx/html/

# Copy the "assets" folder into the NGINX web root directory
COPY ./assets /usr/share/nginx/html/assets

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start NGINX when the container runs
CMD ["nginx", "-g", "daemon off;"]
