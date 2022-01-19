import config
from edamino import Bot, Context, logger
from edamino.api import InvalidRequest

bot = Bot(email=config.EMAIL, password=config.PASSWORD, prefix="/")

@bot.on_ready
async def on_ready():
    logger.info('Ready.')


@bot.command('pin')
async def echo(ctx: Context):
    await ctx.client.edit_chat(
        chat_id=ctx.msg.threadId,
        announcement='lalala',
        pin_announcement=True,
    )
    await ctx.client.set_view_only_chat(ctx.msg.threadId, 'disable')


@bot.command('send')
async def on_int(ctx: Context, coins: int, link: str):
    pass

@bot.command('del')
async def on_clear(ctx: Context):
    msg = await ctx.reply('Good!')
    try:
        await ctx.reply("d" * 2003)
    except InvalidRequest as e:
        await ctx.reply(e.message)

if __name__ == '__main__':
    bot.start()
