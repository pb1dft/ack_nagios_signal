import yaml


COMMENTS = {
    'signal_number': 'Define the number which is attached to the bot',
    'websocket_url': 'Define the websocket url to listen for messages',
    'signal_api_url': 'Define the api url to send various commands',
    'nagios_cmd_file': 'Define the nagios cmd file to send commands to nagios',
    'pending_users_file': 'Define the pending user file for dynamic user management',
    'pending_groups_file': 'Define the pending user file for dynamic user management',
    'pid_file': 'Define the pid file for daemon process',
    'dynamic_user_management': 'Allow dynamic user management',
    'dynamic_group_management': 'Allow dynamic group management',
    'log_level': 'Set the log level (Default: INFO)',
    'group_lock': (
        'Allowed groups locked\n'
        'Set this to true to lock groups to the list of groups in allowed_groups\n'
        'Since we need to build the groups first and fetch the id set this to false on the first run'
    ),
    'allowed_senders': (
        'Define the list of authorized senders\n'
        'When uuid is unknown start the bot and sent the !info command.\n'
        'Example user format (commented out, do not touch here):\n'
        'allowed_senders:\n'
        '  - name: Jenny Doe / Tommy Tutone\n'
        '    number: +15558675309\n'
        '    uuid: 550e8400-e29b-41d4-a716-446655440000'
    ),
    'allowed_groups': 'Define list of groups to receive/process messages in'
}


def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def write_comment_block(comment):
    """Ensure all lines are prefixed with # for proper YAML comment formatting."""
    if isinstance(comment, str):
        comment_lines = comment.strip().splitlines()
    elif isinstance(comment, list):
        comment_lines = comment
    else:
        return []

    return [f'# {line}' for line in comment_lines]


def indent_lines(text, indent=2):
    indentation = ' ' * indent
    return '\n'.join(indentation + line if line.strip() != '' else '' for line in text.splitlines())


def save_config(config: dict, path='config.yaml'):
    lines = []
    for key, value in config.items():
        # Add comment if any
        comment = COMMENTS.get(key)
        if comment:
            lines.extend(write_comment_block(comment))

        if isinstance(value, (list, dict)):
            # Dump ONLY the value (not key:value) with indent=2 and flow style off
            yaml_str = yaml.dump(value, default_flow_style=False, indent=2).rstrip()
            lines.append(f'{key}:')
            # indent the dumped block by 2 spaces
            lines.append(indent_lines(yaml_str, indent=2))
        else:
            # Format simple types manually
            if isinstance(value, str):
                value_str = f"'{value}'"
            elif isinstance(value, bool):
                value_str = 'true' if value else 'false'
            elif value is None:
                value_str = 'null'
            else:
                value_str = str(value)
            lines.append(f'{key}: {value_str}')

        lines.append('')  # Blank line after each key for readability

    with open(path, 'w') as f:
        f.write('\n'.join(lines))
