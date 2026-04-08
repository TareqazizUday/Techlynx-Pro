"""
Gunicorn configuration file for Techlynx Pro
"""
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/gunicorn/techlynxpro-access.log"
errorlog = "/var/log/gunicorn/techlynxpro-error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "techlynxpro"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/techlynxpro.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# Auto-restart on worker death
max_requests = 1000
max_requests_jitter = 50
# False: each worker loads the app (more RAM); avoids stale code after deploy when using worker recycling.
# True: faster fork, but ensure you always `systemctl restart techlynxpro` after code upload.
preload_app = False

# SSL (uncomment if using SSL)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

