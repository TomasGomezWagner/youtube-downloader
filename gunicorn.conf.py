# Gunicorn configuration file
import multiprocessing

# Worker timeout - 5 minutos para descargas grandes
timeout = 300

# Workers - solo 1 para evitar conflictos con descargas
workers = 1

# Bind
bind = "0.0.0.0:10000"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Keep alive
keepalive = 120

# Preload app
preload_app = False
