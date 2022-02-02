import time

import random

from edamino import Context, logger
from edamino.objects import UserProfile

from config import bot

logger.setLevel('DEBUG')


@bot.event()
async def on_ready(profile: UserProfile):
    logger.info(f'{profile.nickname} ready.')


@bot.event()
async def on_mention(ctx: Context):
    await ctx.reply('lala')


@bot.command(['ping', 'pong'])
async def on_ping(ctx: Context):
    async with ctx.recording():
        await ctx.reply('Pong!')


@bot.command('бибаметр')
async def on_biba(ctx: Context):
    async with ctx.typing():
        await ctx.reply(f'Ваш размер {random.randint(1, 10000)} см.')


@bot.command('speedtest')
async def on_speed(ctx: Context):
    timestamp = time.time()
    await ctx.reply('.')
    await ctx.reply(f'Время обработки {time.time() - timestamp:.2f}s.')


@bot.command('send')
async def on_send(ctx: Context, coins: int, link: str):
    await ctx.reply(f'{coins} {link}')


# S.c say 500 aboba play tv

@bot.command('say')
async def _(ctx: Context, args: str):
    await ctx.reply(args)


bot.start()
