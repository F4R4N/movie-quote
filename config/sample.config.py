CONFIG_DEBUG = True
CONFIG_SECRET_KEY = "a_secret_key_here_remember_to_change_it_On_Deployment"

# use in deployment
CONFIG_SECURE_SSL_REDIRECT = True
CONFIG_SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
