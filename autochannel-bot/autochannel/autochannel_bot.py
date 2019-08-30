#!/usr/bin/env python3
"""
Tamago BOT LIVES!
"""
import asyncio
import random
import os
import discord
import importlib
import logging
import coloredlogs
import sys
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from autochannel.lib import plugin, utils
from autochannel.autochannel import AutoChannel

EXTENSIONS = [
    'autochannels',
    'server',
    ]

LOG = logging.getLogger(__name__)

APP_ID = os.getenv('APP_ID') or 'fakeid'
BOT_PREFIX = ("?", "!")
SHARD = os.getenv('SHARD') or 0
SHARD_COUNT = os.getenv('SHARD_COUNT') or 1
TOKEN = os.getenv('TOKEN')
VOICE_CHANNEL_PREFIX = os.getenv('VOICE_CHANNEL_PREFIX') or '!VC '
AUTO_CHANNEL_PREFIX = os.getenv('AUTO_CHANNEL_PREFIX') or '!AC '
AUTO_CATEGORIES = os.getenv('AUTO_CATEGORIES').lower().split(",") or ['auto-voice']
DD_API_KEY = os.getenv('DD_API_KEY') or None
DD_APP_KEY = os.getenv('DD_APP_KEY') or None
ENV = os.getenv('ENV') or None

def main():
    """Entrypoint if called as an executable."""
    args = utils.parse_arguments()
    logging.basicConfig(level=logging.INFO)
    coloredlogs.install(level=0,
                        fmt="[%(asctime)s][%(levelname)s] [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                        isatty=True)
    if args.debug:
        l_level = logging.DEBUG
    else:
        l_level = logging.INFO

    logging.getLogger(__package__).setLevel(l_level)
    logging.getLogger('discord').setLevel(l_level)
    logging.getLogger('websockets.protocol').setLevel(l_level)
    logging.getLogger('urllib3').setLevel(l_level)
    logging.getLogger('datadog').setLevel(l_level)

    LOG.info("LONG LIVE AutoChannel bot")
    autochannel = AutoChannel(shard_id=int(SHARD), shard_count=int(SHARD_COUNT),
                    command_prefix=BOT_PREFIX, app_id=APP_ID, voice_channel_prefix=VOICE_CHANNEL_PREFIX,
                    auto_channel_prefix=AUTO_CHANNEL_PREFIX, auto_categories=AUTO_CATEGORIES,
                    dd_api_key=DD_API_KEY, dd_app_key=DD_APP_KEY, env=ENV)

    for extension in EXTENSIONS:
        plugin.load('autochannel.lib.plugins.{}'.format(extension), autochannel)

    autochannel.run(TOKEN)


if __name__ == '__main__':
    main()
