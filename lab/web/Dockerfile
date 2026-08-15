FROM php:8.3-apache

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libsqlite3-dev \
    && docker-php-ext-install mysqli pdo_sqlite \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/www/html/data \
    && chown -R www-data:www-data /var/www/html/data

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
