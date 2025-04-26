import os  # noqa: E402

from config_loader import save_config  # noqa: E402

import yaml  # noqa: E402


def handle_truncate_users_command(config: dict):
    if not os.path.exists(config.get('pending_users_file')):
        return '📭 No pending users.'

    # Load current pending list
    try:
        with open(config.get('pending_users_file'), 'w') as f:
            yaml.dump([], f)
        return '🧹 Pending users list has been cleared.'
    except Exception as e:
        return f'❗ Error clearing pending users: {e}'


def handle_pending_command(config: dict):
    if not os.path.exists(config.get('pending_users_file')):
        return '📭 No pending users.'

    with open(config.get('pending_users_file'), 'r') as f:
        data = yaml.safe_load(f) or {}

    pending = data.get('pending_users', [])

    if not pending:
        return '📭 No pending users.'

    lines = ['🕒 Pending users:']
    for i, user in enumerate(pending, 1):
        name = user.get('name', 'Unknown')
        uuid = user.get('uuid', 'N/A')
        number = user.get('number', 'N/A')
        lines.append(f'{i}. {name}\n   UUID: {uuid}\n   Number: {number}')

    return '\n'.join(lines)


def handle_approve_command(index: int, config: dict):

    with open(config.get('pending_users_file'), 'r') as f:
        data = yaml.safe_load(f) or {}

    pending = data.get('pending_users', [])

    allowed = config['allowed_senders']

    if index < 1 or index > len(pending):
        return f'❌ Invalid index. Please use a number between 1 and {len(pending)}.', config

    user_to_approve = pending.pop(index - 1)
    user_uuid = user_to_approve.get('uuid')

    # 🔍 Check if already allowed by UUID
    if any(u.get('uuid') == user_uuid for u in allowed):
        with open(config.get('pending_users_file'), 'w') as f:
            yaml.dump({'pending_users': pending}, f)
        return f"⚠️ User already approved: {user_to_approve.get('name', 'Unknown')}", config

    allowed.append(user_to_approve)

    # Update the config dict
    config['allowed_senders'] = allowed

    # Save back to file
    save_config(config)

    # Save pending users
    with open(config.get('pending_users_file'), 'w') as f:
        yaml.dump({'pending_users': pending}, f)

    name = user_to_approve.get('name', 'Unknown')
    return f'✅ Approved user: {name}', config


def list_allowed_users(config):
    message_lines = ['✅ Allowed users:']
    for user in config.get('allowed_senders'):
        name = user.get('name', 'Unknown')
        number = user.get('number', 'N/A')
        uuid = user.get('uuid', 'N/A')
        message_lines.append(f'- Name: {name}, Number: {number}, UUID: {uuid}')

    message = '\n'.join(message_lines)
    return message


def handle_remove_command(target_uuid: str, config: dict):

    initial_len = len(config.get('allowed_senders'))
    filtered_users = [user for user in config.get('allowed_senders') if user.get('uuid') != target_uuid]

    if len(filtered_users) < initial_len:
        config['allowed_senders'] = filtered_users
        save_config(config)  # If you have a save function to persist config
        return f'🗑️  Removed user with UUID: {target_uuid}', config
    else:
        return f'❌ No user found with UUID: {target_uuid}', config
