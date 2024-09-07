"""
    Python Fail2Ban API
    ===================

    A Python API for interacting with Fail2Ban statistics via FastAPI and Pydantic models.

    Copyright (c) 2024 <Denis Rozhnovskiy>
    All Rights Reserved.

    Licensed under the MIT License. You may obtain a copy of the License at:

        https://opensource.org/licenses/MIT

    This software is provided "as is", without warranty of any kind, express or implied,
    including but not limited to the warranties of merchantability, fitness for a particular purpose,
    and noninfringement. In no event shall the authors or copyright holders be liable for any claim,
    damages, or other liability, whether in an action of contract, tort, or otherwise, arising from,
    out of, or in connection with the software or the use or other dealings in the software.

    Module: logger_config.py
    Author: <Denis Rozhnovskiy (https://github.com/orenlab)>

    Description:
    ------------

    This module contains functions for setting up and configuring the logger in JSON format without external libraries.
"""

import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as a JSON object.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: A JSON-formatted string.
        """
        log_record = {
            "levelname": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "filename": record.filename,
            "lineno": record.lineno,
            "asctime": self.formatTime(record, self.datefmt),
        }

        # Add extra attributes if they are provided in record
        if hasattr(record, "extra"):
            log_record.update(record.extra)

        return json.dumps(log_record)


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up and configure the logger in JSON format without external libraries.

    Args:
        name (str): The name of the logger.
        level (int): Logging level, default is INFO.

    Returns:
        logging.Logger: Configured logger in JSON format.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Use custom JSON formatter
        json_formatter = JsonFormatter()
        handler.setFormatter(json_formatter)

        logger.addHandler(handler)

    return logger
