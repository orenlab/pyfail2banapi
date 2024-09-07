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

    Module: app.py
    Author: <Denis Rozhnovskiy (https://github.com/orenlab)>

    Description:
    ------------
    A Python API for interacting with fail2ban statistics via FastAPI and Pydantic models.
"""

import logging

from fastapi import FastAPI, HTTPException, Request
from pydantic import ValidationError

from pyfail2banapi.client import (
    get_fail2ban_status,
    get_jail_status,
    get_fail2ban_version,
    validate_jail_name,
)
from pyfail2banapi.models import Fail2BanStatus, JailStatus, Fail2BanVersion
from pyfail2banapi.parsers import parse_jail_status

app = FastAPI(
    title="Python Fail2Ban API",
    description="A Python API for interacting with fail2ban statistics via FastAPI and Pydantic models.",
    version="0.1.0",
)

from pyfail2banapi.logger_config import setup_logger

logger = setup_logger(__name__, logging.INFO)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log request details and response time in JSON format.
    """
    ip_address = request.client.host
    url = request.url.path
    method = request.method
    headers = dict(request.headers)

    logger.info(
        f"Request received",
        extra={"ip": ip_address, "url": url, "method": method, "headers": headers},
    )

    response = await call_next(request)

    logger.info(
        f"Response sent",
        extra={
            "ip": ip_address,
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "headers": headers,
        },
    )

    return response


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
        raise HTTPException(
            status_code=500, detail="Failed to retrieve fail2ban status"
        )
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
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve status for jail {jail_name}"
        )
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
        raise HTTPException(
            status_code=500, detail="Failed to retrieve fail2ban version"
        )
    except Exception as e:
        logger.error(f"Error retrieving Fail2Ban version: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
