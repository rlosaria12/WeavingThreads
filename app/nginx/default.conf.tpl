 server {
    listen ${LISTEN_PORT};

    location /static {
        alias /vol/static;
    }

    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
        
        # Add the following timeout settings
        proxy_connect_timeout   1800s;
        proxy_read_timeout      1800s;
        proxy_send_timeout      1800s;
        uwsgi_read_timeout      1800s;
    }
}