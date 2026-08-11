FROM php:8.3-apache

# Install MySQL extension
RUN docker-php-ext-install mysqli pdo_mysql

# Copy website
COPY . /var/www/html/

# Fix permissions
RUN chown -R www-data:www-data /var/www/html
