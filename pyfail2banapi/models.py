from typing import List

from pydantic import BaseModel


class Fail2BanStatus(BaseModel):
    """
    Pydantic model representing the overall status of the fail2ban service.
    """
    number_of_jails: int
    jail_list: List[str]


class JailStatus(BaseModel):
    """
    Pydantic model representing the status of a specific jail in fail2ban.
    """
    jail_name: str
    status: str


class Fail2BanVersion(BaseModel):
    """
    Pydantic model representing the version of the fail2ban service.
    """
    version: str


from pydantic import BaseModel
from typing import List


class JailStatusFilter(BaseModel):
    currently_failed: int
    total_failed: int
    file_list: str


class JailStatusActions(BaseModel):
    currently_banned: int
    total_banned: int
    banned_ip_list: List[str]


class JailStatus(BaseModel):
    jail_name: str
    filter: JailStatusFilter
    actions: JailStatusActions
