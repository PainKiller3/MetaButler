# MetaButler/modules/sql/command_usage_sql.py
import threading
import time
from sqlalchemy import Column, String, BigInteger, Integer, func
from MetaButler.modules.sql import BASE, SESSION

class CommandUsage(BASE):
    __tablename__ = "command_usage"
    id = Column(Integer, primary_key=True, autoincrement=True)
    command = Column(String(255), nullable=False)
    chat_id = Column(BigInteger)
    user_id = Column(BigInteger)
    timestamp = Column(Integer, default=lambda: int(time.time()))

    def __init__(self, command, chat_id, user_id):
        self.command = command
        self.chat_id = chat_id
        self.user_id = user_id

CommandUsage.__table__.create(checkfirst=True)

COMMAND_USAGE_LOCK = threading.RLock()

def log_command(command, chat_id, user_id):
    with COMMAND_USAGE_LOCK:
        log = CommandUsage(command, chat_id, user_id)
        SESSION.add(log)
        SESSION.commit()

def get_command_usage():
    try:
        return SESSION.query(CommandUsage.command, func.count(CommandUsage.command).label('count')).group_by(CommandUsage.command).order_by(func.count(CommandUsage.command).desc()).all()
    finally:
        SESSION.close()