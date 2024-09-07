import logging
import subprocess
from typing import Optional

from pyfail2banapi.models import JailStatus, JailStatusActions, JailStatusFilter

logger = logging.getLogger(__name__)

import re
from typing import Dict


def parse_fail2ban_status(status: str) -> Dict[str, any]:
    """
    Parse the status output from fail2ban-client and convert it to a JSON-compatible dictionary.

    Args:
        status (str): The raw status output from fail2ban-client.

    Returns:
        dict: A dictionary containing parsed Fail2Ban status.
    """
    lines = status.split('\n')
    jail_number_line = lines[1].strip()
    jail_list_line = lines[2].strip()

    # Extract the number of jails
    number_of_jails_match = re.search(r'Number of jail:\s*(\d+)', jail_number_line)
    if not number_of_jails_match:
        raise ValueError("Failed to parse number of jails")
    number_of_jails = int(number_of_jails_match.group(1))

    # Extract the list of jails
    jail_list_match = re.search(r'Jail list:\s*(.*)', jail_list_line)
    if not jail_list_match:
        raise ValueError("Failed to parse jail list")
    jail_list = jail_list_match.group(1).split(',')

    return {
        "number_of_jails": number_of_jails,
        "jail_list": [jail.strip() for jail in jail_list]
    }


def parse_jail_status(status: str, jail_name: str) -> JailStatus:
    """
    Parse the jail status output from fail2ban-client and convert it to a Pydantic model.

    Args:
        status (str): The raw status output from fail2ban-client.
        jail_name (str): The name of the jail.

    Returns:
        JailStatus: A Pydantic model containing parsed jail status.

    Raises:
        ValueError: If the status output is incomplete or malformed.
    """
    lines = status.split('\n')

    if len(lines) < 6:
        raise ValueError("The status output is incomplete or malformed.")

    # Initialize default values
    currently_failed = total_failed = currently_banned = total_banned = 0
    file_list = ''
    banned_ip_list = []

    # Extract filter details
    try:
        for line in lines:
            if 'Currently failed:' in line:
                currently_failed = int(line.split(':')[1].strip())
            elif 'Total failed:' in line:
                total_failed = int(line.split(':')[1].strip())
            elif 'File list:' in line:
                file_list = line.split(':')[1].strip()
    except (IndexError, ValueError) as e:
        raise ValueError(f"Error parsing filter details: {e}")

    # Extract actions details
    try:
        for line in lines:
            if 'Currently banned:' in line:
                currently_banned = int(line.split(':')[1].strip())
            elif 'Total banned:' in line:
                total_banned = int(line.split(':')[1].strip())
            elif 'Banned IP list:' in line:
                banned_ip_list = line.split(':')[1].strip().split()
    except (IndexError, ValueError) as e:
        raise ValueError(f"Error parsing actions details: {e}")

    # Create Pydantic models
    filter_data = JailStatusFilter(
        currently_failed=currently_failed,
        total_failed=total_failed,
        file_list=file_list
    )

    actions_data = JailStatusActions(
        currently_banned=currently_banned,
        total_banned=total_banned,
        banned_ip_list=banned_ip_list
    )

    return JailStatus(
        jail_name=jail_name,
        filter=filter_data,
        actions=actions_data
    )


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


def get_fail2ban_status() -> Dict[str, any] | None:
    """
    Retrieve the overall status of the fail2ban service by executing the 'fail2ban-client status' command.

    Returns:
        dict | None: The parsed status data or None if the command fails.
    """
    try:
        result = subprocess.run(
            ['fail2ban-client', 'status'],
            capture_output=True,
            text=True,
            check=True
        )
        return parse_fail2ban_status(result.stdout)
    except FileNotFoundError:
        logger.error("fail2ban-client command not found. Please ensure Fail2Ban is installed.")
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
