import config

from edamino import Bot, Context, logger

bot = Bot(email=config.EMAIL, password=config.PASSWORD)


@bot.event()
async def on_ready():
    logger.info('Ready.')


@bot.event()
async def echo(ctx: Context):
    await ctx.reply(ctx.msg.content)


if __name__ == '__main__':
    bot.start()
