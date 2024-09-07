# Python Fail2Ban API

## Overview

The Python Fail2Ban API is a robust and efficient FastAPI application designed to interact with Fail2Ban statistics. It
provides endpoints to retrieve real-time data on Fail2Ban's overall status, the status of specific jails, and the
Fail2Ban version. This API is particularly well-suited for integration with automation tools and bots, such as Telegram
bots, enabling seamless monitoring and reporting of security metrics.

## Features

- **Retrieve Overall Status**: Access the current status of the Fail2Ban service.
- **Query Jail Status**: Get the status of individual jails within Fail2Ban.
- **Fetch Version Information**: Obtain the version of the Fail2Ban service installed.

## Installation

### Prerequisites

- Python 3.12+
- Uvicorn for serving the FastAPI application
- Fail2Ban installed on your system

### Setup Steps

1. **Create a Virtual Environment**

   It's a best practice to use a virtual environment to manage project dependencies. Create and activate a virtual
   environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install Dependencies**

   Install the necessary Python packages, including the `pyfail2banapi` package:

   ```bash
   poetry add pyfail2banapi --without dev
   ```

3. **Create a Non-Privileged User and Group**

   To run the service securely, create a non-privileged user and group:

   ```bash
   sudo groupadd fail2ban-api
   sudo useradd -g fail2ban-api -m -s /bin/false fail2ban-api
   ```

4. **Adjust File Permissions**

   Ensure that the application directory is owned by the `fail2ban-api` user:

   ```bash
   sudo chown -R fail2ban-api:fail2ban-api /path/to/your/app
   sudo chmod -R 750 /path/to/your/app
   ```

5. **Create the Systemd Service File**

   Set up a systemd service file at `/etc/systemd/system/fail2ban-api.service`:

   ```ini
   [Unit]
   Description=Fail2Ban API Service
   After=network.target

   [Service]
   ExecStart=/path/to/your/venv/bin/uvicorn pyfail2banapi.main:app --host 0.0.0.0 --port 8000
   User=fail2ban-api
   Group=fail2ban-api
   WorkingDirectory=/path/to/your/app
   Environment=PATH=/path/to/your/venv/bin:/usr/bin:/bin
   Restart=always
   RestartSec=5
   LimitNOFILE=4096
   LimitNPROC=512

   [Install]
   WantedBy=multi-user.target
   ```

6. **Reload Systemd and Start the Service**

   Reload systemd to apply changes and start the service:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable fail2ban-api.service
   sudo systemctl start fail2ban-api.service
   ```

## Usage

The API is available at `http://localhost:8000` and provides the following endpoints:

- **GET /status**: Retrieves the overall status of Fail2Ban.
- **GET /status/{jail_name}**: Retrieves the status of a specific jail.
- **GET /version**: Retrieves the version of Fail2Ban.

This API can be integrated with bots, such as Telegram bots, to automate the monitoring and reporting of Fail2Ban status
and statistics.

## Security

- The API runs as a non-privileged user (`fail2ban-api`), enhancing system security.
- Ensure that Fail2Ban is properly configured and that access is restricted as needed.

## Troubleshooting

- Check the status of the service with: `sudo systemctl status fail2ban-api.service`.
- View logs for troubleshooting: `journalctl -u fail2ban-api.service`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome. Please submit issues and pull requests through the GitHub repository.
