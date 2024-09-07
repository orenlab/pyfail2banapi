# Python Fail2Ban API

## Overview

The Python Fail2Ban API is a FastAPI-based application designed to interact with Fail2Ban statistics. It provides
RESTful endpoints to retrieve Fail2Ban’s overall status, individual jail status, and version information, making it
ideal for integrating with automation systems like bots.

## Features

- **Fail2Ban Status**: Retrieve real-time service status.
- **Jail Status**: Query the status of individual jails.
- **Version Information**: Fetch the installed Fail2Ban version.

## Installation

### Prerequisites

- **Python**: Version 3.10 or higher
- **Poetry**: For managing dependencies and the virtual environment
- **Fail2Ban**: Installed on your system

### Setup Instructions

1. **Clone the Repository**

   First, clone the repository as the root user:

   ```bash
   sudo -i
   cd /root
   git clone https://github.com/orenlab/pyfail2banapi.git
   ```

2. **Set Up Poetry Virtual Environment**

   Navigate to the project directory and set up the environment using Poetry:

   ```bash
   cd /root/pyfail2banapi
   poetry install --only main
   ```

3. **Activate the Virtual Environment**

   Activate the environment using Poetry to run the API within the virtual environment:

   ```bash
   poetry shell
   ```

4. **Run the Application**

   Start the FastAPI application using Poetry:

   ```bash
   uvicorn app:app --host 127.0.0.1 --port 8000
   ```

5. **Systemd Service Configuration**

   To run the API as a service from `/root/pyfail2banapi/app.py`, create a systemd service file at
   `/etc/systemd/system/fail2ban-api.service`:

   ```ini
   [Unit]
   Description=Fail2Ban API Service
   After=network.target

   [Service]
   ExecStart=/root/.venv/bin/uvicorn pyfail2banapi.app:app --host 127.0.0.1 --port 8000
   User=root
   Group=root
   WorkingDirectory=/root/pyfail2banapi
   Restart=always
   RestartSec=5
   LimitNOFILE=4096
   LimitNPROC=512

   [Install]
   WantedBy=multi-user.target
   ```

6. **Reload and Start the Service**

   Reload systemd and start the service:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable fail2ban-api.service
   sudo systemctl start fail2ban-api.service
   ```

## Usage

Once the service is running, the API will be available at `http://127.0.0.1:8000`.

### Available Endpoints:

- **GET /status**: Get the overall Fail2Ban status.
- **GET /status/{jail_name}**: Get the status of a specific jail.
- **GET /version**: Retrieve the Fail2Ban version.

## Security Best Practices

- Run the service in a secure, isolated environment.
- Use HTTPS when deploying in production environments.
- Ensure Fail2Ban is configured properly and restrict access to the API.

## Contribution

Contributions are welcome! See the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this
project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Troubleshooting

- To check service status: `sudo systemctl status fail2ban-api.service`
- To view logs: `journalctl -u fail2ban-api.service`
