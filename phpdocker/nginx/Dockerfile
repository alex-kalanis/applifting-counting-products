FROM nginx:alpine
WORKDIR "/application"

# Fix debconf warnings upon build
ARG PHP_UID=1000
ARG PHP_GID=1000

RUN apk update
RUN apk add shadow

# Aliases php to use as UID:GID = 1000:1000
# Needed when using console because of privileges on cache dir from web

RUN groupadd -g ${PHP_GID} php_console
RUN useradd -u ${PHP_UID} -g ${PHP_GID} php_console

# php console can run things for group nginx
RUN usermod -a -G nginx php_console
# nginx can run things for group php console
RUN usermod -a -G php_console nginx
# aliases for running scripts
