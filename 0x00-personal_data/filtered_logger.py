#!/usr/bin/env python3
""" Module to filter log messages """

import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = []):
        """ Constructor method
            """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format method
            """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(
                fields: List[str],
                redaction: str,
                message: str,
                separator: str
                ) -> str:
    """ Returns a log message """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a logger object """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to the database """
    connector = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME') or 'root',
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD') or '',
        host=os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost',
        database=os.getenv('PERSONAL_DATA_DB_NAME'))
    return connector
