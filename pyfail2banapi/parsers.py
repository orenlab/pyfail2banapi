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

    Module: parsers.py
    Author: <Denis Rozhnovskiy (https://github.com/orenlab)>

    Description:
    ------------

    This module contains functions for parsing the status output from fail2ban-client and
    converting it to a JSON-compatible dictionary.
"""

import re

from pyfail2banapi.models import JailStatus, JailStatusActions, JailStatusFilter


def parse_fail2ban_status(status: str) -> dict:
    """
    Parse the status output from fail2ban-client and convert it to a JSON-compatible dictionary.

    Args:
        status (str): The raw status output from fail2ban-client.

    Returns:
        dict: A dictionary containing parsed Fail2Ban status.

    Raises:
        ValueError: If the output cannot be parsed properly.
    """
    lines = status.split("\n")

    # Validate status structure
    if len(lines) < 3:
        raise ValueError("Incomplete Fail2Ban status output")

    jail_number_line = lines[1].strip()
    jail_list_line = lines[2].strip()

    # Extract the number of jails
    number_of_jails_match = re.search(r"Number of jail:\s*(\d+)", jail_number_line)
    if not number_of_jails_match:
        raise ValueError("Failed to parse number of jails")
    number_of_jails = int(number_of_jails_match.group(1))

    # Extract the list of jails
    jail_list_match = re.search(r"Jail list:\s*(.*)", jail_list_line)
    if not jail_list_match:
        raise ValueError("Failed to parse jail list")
    jail_list = jail_list_match.group(1).split(",")

    return {
        "number_of_jails": number_of_jails,
        "jail_list": [jail.strip() for jail in jail_list],
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
    lines = status.split("\n")

    if len(lines) < 6:
        raise ValueError("The status output is incomplete or malformed.")

    # Initialize default values
    currently_failed = total_failed = currently_banned = total_banned = 0
    file_list = ""
    banned_ip_list = []

    try:
        for line in lines:
            # Parse filter details
            if "Currently failed:" in line:
                currently_failed = int(line.split(":")[1].strip())
            elif "Total failed:" in line:
                total_failed = int(line.split(":")[1].strip())
            elif "File list:" in line:
                file_list = line.split(":")[1].strip()

            # Parse actions details
            elif "Currently banned:" in line:
                currently_banned = int(line.split(":")[1].strip())
            elif "Total banned:" in line:
                total_banned = int(line.split(":")[1].strip())
            elif "Banned IP list:" in line:
                banned_ip_list = line.split(":")[1].strip().split()
    except (IndexError, ValueError) as e:
        raise ValueError(f"Error parsing jail status: {e}")

    # Create Pydantic models
    filter_data = JailStatusFilter(
        currently_failed=currently_failed,
        total_failed=total_failed,
        file_list=file_list,
    )

    actions_data = JailStatusActions(
        currently_banned=currently_banned,
        total_banned=total_banned,
        banned_ip_list=banned_ip_list,
    )

    return JailStatus(jail_name=jail_name, filter=filter_data, actions=actions_data)


def validate_jail_name(jail_name: str) -> bool:
    """
    Validate the jail name to ensure it contains only safe characters.

    Args:
        jail_name (str): The jail name to validate.

    Returns:
        bool: True if the jail name is valid, False otherwise.
    """
    return re.match("^[a-zA-Z0-9_-]+$", jail_name) is not None
