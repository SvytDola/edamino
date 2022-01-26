import config

from edamino import Bot, Context, logger

bot = Bot(email=config.EMAIL, password=config.PASSWORD, prefix="/")


@bot.event()
async def on_ready():
    logger.info('Ready.')


@bot.command('ping')
async def on_ping(ctx: Context):
    async with ctx.typing():
        await ctx.reply('Pong!')


if __name__ == '__main__':
    bot.start()
