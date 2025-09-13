# gunicorn.conf.py
accesslog = None  # Disable access logs
loglevel = 'info'  # Set the log level for errors and general logs
disable_logger = True  # Disable Gunicorn's logging

print("Gunicorn configuration loaded")