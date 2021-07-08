:: this is a sample of environment variable use for deployment run "cmd /C env.cmd" to activate
SET CONFIG_SECRET_KEY=secret_key
SET CONFIG_DEBUG=0
SET CONFIG_SECURE_SSL_REDIRECT=1
SET CONFIG_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO, https
SET CONFIG_ALLOWED_HOSTS=127.0.0.1, localhost
SET DB=db_name
SET DB_USER=db_user
SET DB_PASSWORD=db_password
SET DB_HOST=db_hostname
SET DB_PORT=db_port
SET IPSTACK_ACCESS_KEY=your_access_key
echo "all environment variables are set"
