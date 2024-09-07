from pydantic import BaseModel


class Fail2BanStatus(BaseModel):
    """
    Pydantic model representing the fail2ban service status.
    """
    status: str


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
