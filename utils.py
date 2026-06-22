from aiogram.types import BotCommand


def get_admin_cmd():
    return BotCommand(command='admin', description='Команда главаря')

