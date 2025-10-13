#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Substitute specified environment variables in the configuration template
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Start nginx
nginx -g 'daemon off;'
