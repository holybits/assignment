"""
Logging Config, imported at the end of common.py
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s',
            # 'datefmt': '%H:%M:%S',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s',
            # 'datefmt': '%d-%m-%Y %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true', 'request_id'],
        },
        'django_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            "maxBytes": 52428800,
            "backupCount": 5,
            "encoding": "utf8",
            'filters': ['request_id'],
        },
        'exceptions_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'exceptions.log'),
            "maxBytes": 52428800,
            "backupCount": 5,
            "encoding": "utf8",
            'filters': ['request_id'],
        },

        'primary_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'primary.log'),
            "maxBytes": 52428800,
            "backupCount": 20,
            "encoding": "utf8",
            'filters': ['request_id'],
        },



    },
    'loggers': {
        'django.request': {
            'handlers': ['exceptions_file'],
            'level': 'DEBUG',
            'propagate': False,
        },

        'primary': {
            'handlers': ['primary_file'],
            'level': 'DEBUG',
        },



        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # },
    },
}