# ack_nagios_signal

## Description

ack_nagios_signal is a Python bot that allows users to acknowledge Nagios problems and control Nagios notifications via Signal messenger.

It listens for specific commands sent through Signal and interacts with the Nagios command file accordingly.
The bot supports dynamic management of allowed users and groups, and can be run as a daemon.

## Features

- Acknowledge Nagios service and host problems by replying to Signal alerts.
- Enable/Disable global Nagios notifications.
- Send various administrative commands via Signal (!reload, !loglevel, etc.).
- Dynamic user and group management (pending approvals through Signal).
- Systemd journal integration for logging.
- Websocket integration for real-time message handling.
- Daemonization support.

## Setup

* 1 Using a venv   
  * 1.1 Create the venv   
    ```bash
       python3 -m venv ack_nagios_signal
    ```

  * 1.2 Clone the Repository   
    ```bash
       git clone https://github.com/pb1dft/ack_nagios_signal/
       cd ack_nagios_signal
    ```
  * 1.3 Install Requirements   
    ```bash
    pip install -r requirements.txt
    ```
* 2 Using a RHEL based system with default packages
  * 2.1 Clone the Repository   
    ```bash
       git clone https://github.com/pb1dft/ack_nagios_signal/
       cd ack_nagios_signal
    ```
  * 2.2 Install Requirements   
    ```bash
    sudo dnf install -y $(cat fedora-packages.txt)
    ```  
3. Configuration

   Edit your configuration file (config.yaml or whatever load_config() loads).
   Set the following:

   - signal_number: Your Signal bot number
   - signal_api_url: URL to your Signal API server
   - websocket_url: WebSocket URL for Signal message stream
   - nagios_cmd_file: Path to your Nagios command file (e.g., /var/lib/nagios3/rw/nagios.cmd)
   - pid_file: Path to your programs pid file (e.g., /var/run/ack_nagios_signal.pid)
   - allowed_senders: List of allowed users (numbers or UUIDs)
   - allowed_groups: List of allowed Signal group IDs
   - group_lock: When set to true prohibit addition of extra groups (Keep false on first run when you want groups)
   - dynamic_user_management: true or false
   - dynamic_group_management: true or false

4. Run the bot
   * Note: when running in venv don't forget to activate it with
     ```bash
     source ack_nagios_signal/bin/activate
     ```

   - Foreground (for testing):
     ```bash
     ./ack_nagios_signal --foreground
     ```
   - Daemonized:
     ```bash
     ./ack_nagios_signal
     ```
6. Signals

   To stop the daemon, simply send a termination signal (kill <pid> or Ctrl+C if foreground).

## Commands (via Signal)

| Command | Description |
|---------|-------------|
| !ack <comment> | Acknowledge a Nagios alert (must reply to the alert message). |
| !on <reason> | Enable Nagios notifications. |
| !off <reason> | Disable Nagios notifications. |
| !info | Show your user info and optionally request approval. |
| !chatinfo | Show group info and optionally request group approval. |
| !reload | Reload the bot's config from disk. |
| !loglevel <level> | Temporarily change the bot's log level. |https://github.com/bbernhard/signal-cli-rest-api
| !pending_users, !approve_user <int>, !remove_user <uuid>, !truncate_users | Dynamic user management (if enabled). |
| !pending_groups, !approve_groups <int>, !remove_groups <id>, !truncate_groups | Dynamic group management (if enabled). |
| !help | Get a help message with available commands. |

## Project Structure

- ack_nagios_signal      # Main bot script
- config_loader.py       # Loads configuration
- config.yaml            # Main config file
- user_mgmt.py           # Handles user-related actions
- group_mgmt.py          # Handles group-related actions
- requirements.txt       # Python dependencies
- fedora-packages.txt    # Fedora package list

## Requirements

- Python 3.6+
- External services:
  - Signal REST API server (e.g., signal-cli-rest-api (https://github.com/bbernhard/signal-cli-rest-api))
- Python libraries:
  - asyncio
  - websockets
  - requests
  - pyyaml
  - daemonize
  - systemd-python
  - setproctitle
  - logging

(see requirements.txt for details)

## Notes

- You must run the script as a user that has write access to Nagios command file.
- Signal API must be correctly configured and reachable.
- Make sure to regularly update allowed users/groups or enable dynamic management.
- The bot will log to systemd journal by default when running as a daemon.

## License

GNU General Public License v3.0.
See LICENSE for more details.
