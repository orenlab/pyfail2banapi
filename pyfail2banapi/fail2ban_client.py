import logging
import re
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


def validate_jail_name(jail_name: str) -> bool:
    """
    Validate the jail name to ensure it contains only safe characters.

    Args:
        jail_name (str): The jail name to validate.

    Returns:
        bool: True if the jail name is valid, False otherwise.
    """
    # Allow only alphanumeric characters, underscores, and hyphens
    return bool(re.match(r'^[\w-]+$', jail_name))


def handle_subprocess_error(e: subprocess.CalledProcessError, command: str) -> None:
    """
    Handle errors raised by subprocess commands.

    Args:
        e (subprocess.CalledProcessError): The error raised by subprocess.
        command (str): The command that caused the error.
    """
    logger.error(f"Command '{command}' failed with exit code {e.returncode}: {e.stderr.strip()}")


def get_fail2ban_status() -> Optional[str]:
    """
    Retrieve the overall status of the fail2ban service by executing the 'fail2ban-client status' command.

    Returns:
        Optional[str]: The status output from the fail2ban client or None if the command fails.
    """
    command = 'fail2ban-client status'
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        logger.error("fail2ban-client command not found. Please ensure Fail2Ban is installed.")
    except subprocess.CalledProcessError as e:
        handle_subprocess_error(e, command)
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

    command = f'fail2ban-client status {jail_name}'
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        logger.error("fail2ban-client command not found. Please ensure Fail2Ban is installed.")
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
    command = 'fail2ban-client version'
    try:
        result = subprocess.check_output(
            command.split(),
            text=True
        ).strip()
        return result
    except FileNotFoundError:
        logger.error("fail2ban-client command not found. Please ensure Fail2Ban is installed.")
    except subprocess.CalledProcessError as e:
        handle_subprocess_error(e, command)
    except Exception as e:
        logger.error(f"Error retrieving fail2ban version: {e}")
    return None
