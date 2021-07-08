# this is a sample of environment variable use for deployment run "source env.sh" to activate
export CONFIG_SECRET_KEY=secret_key
export CONFIG_DEBUG=0
export CONFIG_SECURE_SSL_REDIRECT=1
export CONFIG_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO, https
export CONFIG_ALLOWED_HOSTS=127.0.0.1, localhost
export DB=db_name
export DB_USER=db_user
export DB_PASSWORD=db_password
export DB_HOST=db_hostname
export DB_PORT=db_port
export IPSTACK_ACCESS_KEY=your_access_key
echo "all environment variables are set"
