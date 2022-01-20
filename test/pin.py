import config
from edamino import Bot, Context, logger
from edamino.api import InvalidRequest

bot = Bot(email=config.EMAIL, password=config.PASSWORD, prefix="/")


@bot.event()
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


from pprint import pprint


@bot.command('bubble')
async def on_int(ctx: Context, text: str):
    bubble = await ctx.client.get_message_info(ctx.msg.threadId, ctx.msg.messageId)
    pprint(ctx.msg.dict())
    # pprint(bubble.dict())


@bot.command('del')
async def on_clear(ctx: Context):
    msg = await ctx.reply('Good!')
    try:
        await ctx.reply("d" * 2003)
    except InvalidRequest as e:
        await ctx.reply(e.message)


if __name__ == '__main__':
    bot.start()
