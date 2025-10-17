# MetaButler/modules/command_stats.py
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from MetaButler.modules.helper_funcs.decorators import metacmd
from MetaButler.modules.sql import command_usage_sql as sql
from MetaButler.modules.helper_funcs.chat_status import dev_plus
from MetaButler.modules.helper_funcs.misc import upload_text

@metacmd(command='commandstats')
@dev_plus
def command_stats(update: Update, context: CallbackContext):
    usage = sql.get_command_usage()
    if not usage:
        update.effective_message.reply_text("No command usage tracked yet.")
        return

    reply = "<b>Command Usage Statistics:</b>\n\n"
    for command, count in usage:
        reply += f"- <code>/{command}</code>: {count} times\n"

    if len(reply) > 4096:
        url = upload_text(reply)
        if url:
            update.effective_message.reply_text(f"Command usage statistics are too long. You can view them here: {url}")
        else:
            update.effective_message.reply_text("Could not upload command statistics.")

    else:
        update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)

__mod_name__ = "Command Stats"