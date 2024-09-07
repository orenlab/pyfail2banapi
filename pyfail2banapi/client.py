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

    Module: client.py
    Author: <Denis Rozhnovskiy (https://github.com/orenlab)>

    Description:
    ------------

    This module contains functions for interacting with the fail2ban service via the 'fail2ban-client' command.
"""

import logging
import subprocess
from typing import Optional

from pyfail2banapi.logger_config import setup_logger
from pyfail2banapi.parsers import parse_fail2ban_status, validate_jail_name

logger = setup_logger(__name__, logging.INFO)


def handle_subprocess_error(e: subprocess.CalledProcessError, command: str) -> None:
    """
    Handle errors raised by subprocess commands.

    Args:
        e (subprocess.CalledProcessError): The error raised by subprocess.
        command (str): The command that caused the error.
    """
    logger.error(
        f"Command '{command}' failed with exit code {e.returncode}: {e.stderr.strip()}"
    )


def get_fail2ban_status() -> Optional[dict]:
    """
    Retrieve the overall status of the fail2ban service by executing the 'fail2ban-client status' command.

    Returns:
        dict | None: The parsed status data or None if the command fails.
    """
    try:
        result = subprocess.run(
            ["fail2ban-client", "status"], capture_output=True, text=True, check=True
        )
        return parse_fail2ban_status(result.stdout)
    except FileNotFoundError:
        logger.error(
            "fail2ban-client command not found. Please ensure Fail2Ban is installed."
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"fail2ban-client command failed: {e.stderr.strip()}")
    except Exception as e:
        logger.error(f"Error retrieving fail2ban status: {e}")
    return None


def get_jail_status(jail_name: str) -> Optional[str]:
    """
    Retrieve the status of a specific jail by executing the 'fail2ban-client status <jail_name>' command.

    Args:
        jail_name (str): The name of the jail to retrieve status for.

    Returns:
        Optional[str]: The status output for the jail from the fail2ban client or None if the command fails.
    """
    if not validate_jail_name(jail_name):
        logger.error(f"Invalid jail name provided: {jail_name}")
        return None

    command = f"fail2ban-client status {jail_name}"
    try:
        result = subprocess.run(
            command.split(), capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        logger.error(
            "fail2ban-client command not found. Please ensure Fail2Ban is installed."
        )
    except subprocess.CalledProcessError as e:
        handle_subprocess_error(e, command)
    except Exception as e:
        logger.error(f"Error retrieving jail status for {jail_name}: {e}")
    return None


def get_fail2ban_version() -> Optional[str]:
    """
    Retrieve the version of the fail2ban service by executing the 'fail2ban-client version' command.

    Returns:
        Optional[str]: The version output from the fail2ban client or None if the command fails.
    """
    command = "fail2ban-client version"
    try:
        result = subprocess.check_output(command.split(), text=True).strip()
        return result
    except FileNotFoundError:
        logger.error(
            "fail2ban-client command not found. Please ensure Fail2Ban is installed."
        )
    except subprocess.CalledProcessError as e:
        handle_subprocess_error(e, command)
    except Exception as e:
        logger.error(f"Error retrieving fail2ban version: {e}")
    return None
