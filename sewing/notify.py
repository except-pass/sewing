# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/notify.ipynb (unless otherwise specified).

__all__ = ['logger', 'yesterday', 'Retriever', 'send_content']

# Cell
import datetime
import logging
logger = logging.getLogger()

from .mailer import send
from .db import get_guild_emails
import sewing.display

# Cell

def yesterday():
    now = datetime.datetime.now()
    return now - datetime.timedelta(days=1)


class Retriever:
    def __init__(self, after=None):
        self.after = after

    async def get_all_messages_in_channel(self, chan):
        '''
        Returns all messages in all open threads in the channel
        That were sent since `after`
        '''
        messages = {}
        all_threads = [] if chan.threads is None else chan.threads
        for thread in all_threads:
            logger.info("THREAD {}".format(thread))
            messages[thread] = await self.get_all_messages_in_thread(thread)
        return messages

    async def get_all_messages_in_thread(self, thread):
            messages = await self.retrieve(thread)
            for msg in messages:
                logger.info("{}".format(msg))
            return messages

    async def retrieve(self, messagable, after=None, **kwargs):
        '''
        messagable = thread or channel
        See other kwargs
        https://discordpy.readthedocs.io/en/stable/api.html#discord.TextChannel.history
        '''
        after = after or self.after or yesterday()
        messages = await messagable.history(after=after, **kwargs).flatten()
        return messages


# Cell

def send_content(content:dict, guild:discord.Guild):
    to_emails = get_guild_emails(guild)
    html_content = sewing.display.html_content(content)
    subject = '[{}] Daily Thread Summary'.format(guild.name)
    return send(to_emails, subject, html_content)