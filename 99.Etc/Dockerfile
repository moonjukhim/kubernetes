FROM php:7.3.3-apache 
RUN apt-get update && apt-get upgrade -y  --allow-unauthenticated 
RUN docker-php-ext-install mysqli 
COPY index.php /var/www/html
EXPOSE 8080
