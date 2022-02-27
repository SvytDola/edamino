import time

import random
from asyncio import sleep

from edamino import Context, logger, Client, api
from edamino.objects import UserProfile, SocketAnswer

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


@bot.command('say')
async def _(ctx: Context, args: str):
    await ctx.reply(args)


@bot.command('count')
async def on_count(ctx: Context):
    response = await ctx.client.request("GET",
                                        f"live-layer?topic=ndtopic%3A{ctx.client.ndc_id}%3Aonline-members&start=0&size=1")
    await ctx.reply(str(response["userProfileCount"]))


def f(s: SocketAnswer):
    return s.o.channelKey is not None


@bot.command('start')
async def on_check(ctx: Context):
    await ctx.join_thread(1)
    await ctx.join_channel(5)
    image = await ctx.download_from_link(
        'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Gull_portrait_ca_usa.jpg/1280px-Gull_portrait_ca_usa.jpg'
    )
    background = await ctx.client.upload_media(image, api.ContentType.IMAGE_JPG)

    await ctx.play_video(background, '/storage/emulated/0/Download/video.mp4', 'video.mp4', 300)
    s = await bot.wait_for(f)
    print(s.o)
    await ctx.play_video_is_done(background, '/storage/emulated/0/Download/video.mp4', 'video.mp4', 300)


@bot.background_task
async def say(client: Client):
    try:
        communities = await client.get_my_communities(size=10)
        client.set_ndc(communities[0].ndcId)
        await client.check_in()
        logger.info('Check in.')
    except api.InvalidRequest as e:
        logger.info(e.message)
    finally:
        await sleep(24 * 60 * 60)


bot.start()
