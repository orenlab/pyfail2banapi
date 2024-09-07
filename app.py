import logging

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from pyfail2banapi.fail2ban_client import get_fail2ban_status, get_jail_status, get_fail2ban_version, \
    validate_jail_name, parse_jail_status
from pyfail2banapi.models import Fail2BanStatus, JailStatus, Fail2BanVersion

app = FastAPI(
    title="Python Fail2Ban API",
    description="A Python API for interacting with fail2ban statistics via FastAPI and Pydantic models.",
    version="0.1.0"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/status", response_model=Fail2BanStatus)
async def fetch_fail2ban_status():
    """
    Fetch the overall status of fail2ban.

    Returns:
        Fail2BanStatus: The status of the fail2ban service.

    Raises:
        HTTPException: If fail2ban status cannot be retrieved.
    """
    try:
        status = get_fail2ban_status()
        if status:
            return Fail2BanStatus(**status)
        raise HTTPException(status_code=500, detail="Failed to retrieve fail2ban status")
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=500, detail="Data validation error")


@app.get("/status/{jail_name}", response_model=JailStatus)
async def fetch_jail_status(jail_name: str):
    """
    Fetch the status of a specific jail.

    Args:
        jail_name (str): The name of the jail to retrieve status for.

    Returns:
        JailStatus: The status of the specified jail.

    Raises:
        HTTPException: If jail status cannot be retrieved.
    """
    if not validate_jail_name(jail_name):
        logger.error(f"Invalid jail name provided: {jail_name}")
        raise HTTPException(status_code=400, detail="Invalid jail name provided")

    try:
        status = get_jail_status(jail_name)
        if status:
            parsed_status = parse_jail_status(status, jail_name)
            return parsed_status
        raise HTTPException(status_code=500, detail=f"Failed to retrieve status for jail {jail_name}")
    except (ValueError, ValidationError) as e:
        logger.error(f"Parsing or validation error: {e}")
        raise HTTPException(status_code=500, detail="Data validation error")


@app.get("/version", response_model=Fail2BanVersion)
async def fetch_fail2ban_version():
    """
    Retrieve the version of Fail2Ban.

    Returns:
        Fail2BanVersion: The version of Fail2Ban.

    Raises:
        HTTPException: If fail2ban version cannot be retrieved.
    """
    try:
        version = get_fail2ban_version()
        if version:
            return Fail2BanVersion(version=version)
        raise HTTPException(status_code=500, detail="Failed to retrieve fail2ban version")
    except Exception as e:
        logger.error(f"Error retrieving Fail2Ban version: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
