from edamino import Bot, Context, logger

from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

bot = Bot(email=getenv('email'), password=getenv('password'))


@bot.on_ready
async def on_ready():
    logger.info('Ready.')


@bot.event()
async def echo(ctx: Context):
    await ctx.reply(ctx.msg.content)


if __name__ == '__main__':
    bot.start()
