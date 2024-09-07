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

    Module: models.py
    Author: <Denis Rozhnovskiy (https://github.com/orenlab)>

    Description:
    ------------

    This module defines the data models used in the API.
"""

from typing import List

from pydantic import BaseModel


class Fail2BanStatus(BaseModel):
    """
    Represents the overall status of the fail2ban service.

    Attributes:
        number_of_jails (int): The total number of jails currently configured in fail2ban.
        jail_list (List[str]): A list of names of the configured jails.
    """

    number_of_jails: int
    jail_list: List[str]


class JailStatus(BaseModel):
    """
    Represents the status of a specific jail in fail2ban.

    Attributes:
        jail_name (str): The name of the jail.
        status (str): The current status of the jail as a string.
    """

    jail_name: str
    status: str


class Fail2BanVersion(BaseModel):
    """
    Represents the version of the fail2ban service.

    Attributes:
        version (str): The version string of the fail2ban service.
    """

    version: str


class JailStatusFilter(BaseModel):
    """
    Represents filter statistics for a specific jail in fail2ban.

    Attributes:
        currently_failed (int): The number of currently failed login attempts.
        total_failed (int): The total number of failed login attempts.
        file_list (str): A list of files being monitored for this jail.
    """

    currently_failed: int
    total_failed: int
    file_list: str


class JailStatusActions(BaseModel):
    """
    Represents actions statistics for a specific jail in fail2ban.

    Attributes:
        currently_banned (int): The number of currently banned IP addresses.
        total_banned (int): The total number of IP addresses banned since the jail was started.
        banned_ip_list (List[str]): A list of IP addresses currently banned by the jail.
    """

    currently_banned: int
    total_banned: int
    banned_ip_list: List[str]


class JailStatus(BaseModel):
    """
    Represents the detailed status of a specific jail, including both filter and action statistics.

    Attributes:
        jail_name (str): The name of the jail.
        filter (JailStatusFilter): A model containing filter-related statistics.
        actions (JailStatusActions): A model containing actions-related statistics.
    """

    jail_name: str
    filter: JailStatusFilter
    actions: JailStatusActions
