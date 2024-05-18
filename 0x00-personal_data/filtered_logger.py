#!/usr/bin/env python3
""" Module to filter log messages """

import re
from typing import List


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
