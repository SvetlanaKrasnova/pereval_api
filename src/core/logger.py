import os

if not os.path.exists('../logs'):
    os.mkdir('../logs')


FORMAT: str = '[%(levelprefix)s %(asctime)s] | %(message)s'
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'format': FORMAT,
        },
        'simple': {
            'format': '%(levelname)s| %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%z',
        },
        'detailed': {
            'format': '[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s| %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%z',
        },
    },
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stderr',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': '../logs/pereval.log',
            'maxBytes': 10000,
            'backupCount': 3,
        },
    },
    'loggers': {
        'pereval': {
            'level': 'DEBUG',
            'handlers': [
                'stderr',
                'file',
            ],
        },
    },
}
