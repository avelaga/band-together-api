FROM python:3.7

RUN mkdir /code/
WORKDIR /code/
COPY . /code/

ENV PYTHONUNBUFFERED 1

ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    postgresql-client \
    apt-utils \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3-pip \
    python3-setuptools \
    python3-virtualenv \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /requirements.txt

RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    python3.7-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip3 install --no-cache-dir -r /requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./Certs/bandtogetherapi_xyz/bandtogetherapi_xyz.crt /etc/apache2/ssl/bandtogetherapi_xyz.crt
COPY ./Certs/bandtogetherapi_xyz/bandtogether-xyz.key /etc/apache2/ssl/bandtogether-xyz.key
COPY ./Certs/bandtogetherapi_xyz/bandtogetherapi_xyz.ca-bundle /etc/apache2/ssl/bandtogetherapi_xyz.ca-bundle
COPY ./default-ssl.conf /etc/apache2/sites-available/default-ssl.conf

RUN a2enmod ssl

RUN echo '. /etc/apache2/envvars' > /root/run_apache.sh && \
 echo 'mkdir -p /var/run/apache2' >> /root/run_apache.sh && \
 echo 'mkdir -p /var/lock/apache2' >> /root/run_apache.sh && \
 echo '/usr/sbin/apache2 -D FOREGROUND' >> /root/run_apache.sh && \
 chmod 755 /root/run_apache.sh

EXPOSE 80
EXPOSE 443

RUN chmod 664 /code/db.sqlite3
RUN chown :www-data /code
RUN chown :www-data /code/db.sqlite3
RUN chown :www-data /code/BandTogetherAPI

CMD /root/run_apache.sh
