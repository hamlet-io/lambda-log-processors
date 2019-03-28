import os
import logging

"""
Map syslog-style log level names (and variations thereof)
to Python log levels.
"""
log_level_map = {
    "EMERG":   logging.CRITICAL,
    "ALERT":   logging.CRITICAL,
    "CRIT":    logging.CRITICAL,
    "ERR":     logging.ERROR,
    "ERROR":   logging.ERROR,
    "WARN":    logging.WARNING,
    "WARNING": logging.WARNING,
    "NOTICE":  logging.WARNING,
    "INFO":    logging.INFO,
    "DEBUG":   logging.DEBUG
}

log_args = {}
log_level = os.environ.get("LOGLEVEL", None)
if log_level:
    log_args['level'] = log_level_map[log_level]

# Try to make this module a drop-in replacement for the built-in 'logging'
basicConfig = logging.basicConfig
getLogger = logging.getLogger

logging.basicConfig(**log_args)
