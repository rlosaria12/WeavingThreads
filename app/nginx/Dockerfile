FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="infosyslystI"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./nginx.conf.tpl /etc/nginx/nginx.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

USER root

RUN mkdir -p /vol/static /var/log/nginx /var/run && \
    chmod 755 /vol/static /var/log/nginx /var/run && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf /var/log/nginx /var/run && \
    chmod +x /run.sh && \
    envsubst < /etc/nginx/nginx.conf.tpl > /etc/nginx/nginx.conf

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]