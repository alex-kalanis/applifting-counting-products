FROM phpdockerio/php:7.4-fpm
WORKDIR "/application"

# Fix debconf warnings upon build
ARG PHP_UID=1000
ARG PHP_GID=1000

RUN apt-get update; \
    apt-get -y --no-install-recommends install \
        php7.4-mbstring \
        php7.4-xml \
        php7.4-xmlrpc \
        php7.4-pgsql \
        php7.4-intl \
        php7.4-redis \
        php7.4-zip \
        php7.4-xdebug \
        php7.4-mcrypt \
        php7.4-memcache \
        php7.4-msgpack \
        php7.4-memcached \
        php7.4-ldap \
        php7.4-yaml \
        php7.4-json; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

RUN update-alternatives --set php /usr/bin/php7.4

# add cli user
RUN groupadd -g ${PHP_GID} php_console
RUN useradd -u ${PHP_UID} -g ${PHP_GID} php_console

RUN usermod -a -G www-data php_console
RUN usermod -a -G php_console www-data

EXPOSE 9000 3000 3001
