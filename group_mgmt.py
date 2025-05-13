"""Handle group management commands such as approval, removal, and listing of allowed groups."""

import os  # noqa: E402

from config_loader import save_config  # noqa: E402

import yaml  # noqa: E402


def handle_truncate_groups_command(config):
    """Remove all allowed groups from the configuration."""
    if not os.path.exists(config.get('pending_groups_file')):
        return '📭 No pending groups.'

    # Load current pending list
    try:
        with open(config.get('pending_groups_file'), 'w') as f:
            yaml.dump([], f)
        return '🧹 Pending groups list has been cleared.'
    except Exception as e:
        return f'❗ Error clearing pending groups: {e}'


def handle_pending_command(config):
    """Display groups that are pending approval."""
    if not os.path.exists(config.get('pending_groups_file')):
        return '📭 No pending groups.'

    with open(config.get('pending_groups_file'), 'r') as f:
        data = yaml.safe_load(f) or {}

    pending = data.get('pending_groups', [])

    if not pending:
        return '📭 No pending groups.'

    lines = ['🕒 Pending groups:']
    for i, user in enumerate(pending, 1):
        name = user.get('name', 'Unknown')
        ext_id = user.get('id', 'N/A')
        int_id = user.get('int_id', 'N/A')
        lines.append(f'{i}. {name}\n   ID: {ext_id}\n   Internal ID: {int_id}')

    return '\n'.join(lines)


def handle_approve_command(index: int, config: dict):
    """Approve a pending group by its index and move it to the allowed list."""
    with open(config.get('pending_groups_file'), 'r') as f:
        data = yaml.safe_load(f) or {}

    pending = data.get('pending_groups', [])

    allowed = config.get('allowed_groups', [])

    if index < 1 or index > len(pending):
        return f'❌ Invalid index. Please use a number between 1 and {len(pending)}.', config

    group_to_approve = pending.pop(index - 1)
    group_int_id = group_to_approve.get('int_id')

    # 🔍 Check if already allowed by ID
    if any(g.get('int_id') == group_int_id for g in allowed):
        with open(config.get('pending_groups_file'), 'w') as f:
            yaml.dump({'pending_groups': pending}, f)
        return f"⚠️ Group already approved: {group_to_approve.get('name', 'Unknown')}", config

    allowed.append(group_to_approve)

    # Update the config dict
    config['allowed_groups'] = allowed

    # Save back to file
    save_config(config)

    # Save pending groups
    with open(config.get('pending_groups_file'), 'w') as f:
        yaml.dump({'pending_groups': pending}, f)

    name = group_to_approve.get('name', 'Unknown')
    return f'✅ Approved group: {name}', config


def list_allowed_groups(config):
    """Print the list of currently allowed groups."""
    message_lines = ['✅ Allowed groups:']
    for group in config.get('allowed_groups'):
        name = group.get('name', 'Unknown')
        int_id = group.get('int_id', 'N/A')
        ext_id = group.get('id', 'N/A')
        message_lines.append(f'- Name: {name}, ID: {ext_id}, Internal ID: {int_id}')

    message = '\n'.join(message_lines)
    return message


def handle_remove_command(message_text: str, config: dict):
    """Remove a group from the allowed list based on message text."""
    allowed_groups = config.get('allowed_groups')
    initial_len = len(allowed_groups)

    # Build a new filtered list
    filtered_groups = [group for group in allowed_groups if group.get('id') != message_text]

    if len(filtered_groups) < initial_len:

        config['allowed_groups'] = filtered_groups
        save_config(config)  # If you have a save function to persist config
        return f'🗑️ Removed group with ID: {message_text}', config
    else:
        return f'❌ No group found with ID: {message_text}', config
