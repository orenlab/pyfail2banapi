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
