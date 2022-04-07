FROM php:7.3.3-apache 
RUN apt-get update && apt-get upgrade -y  --allow-unauthenticated 
RUN docker-php-ext-install mysqli 
RUN apt-get install locales -y
RUN locale-gen ko_KR.UTF-8

# config PHP
ENV TERM xterm

# Apache configuration
RUN a2enmod rewrite
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN sed -i '/<Directory \/var\/www\/>/,/<\/Directory>/ s/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf


# Code copy
COPY index.php /var/www/html/
COPY .htaccess /var/www/html/

EXPOSE 80
