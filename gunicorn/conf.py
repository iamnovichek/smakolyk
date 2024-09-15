workers = 1
bind = "0.0.0.0:8000"
module = "aurigaone.wsgi:application"

# Gunicorn logging configuration
accesslog = "-"
errorlog = "-"
loglevel = "info"