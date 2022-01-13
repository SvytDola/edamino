# edamino
Async api for amino

## Installation: 
`pip install ed-amino`

### Example Bot.
```py
from edamino import Bot, Context, logger

bot = Bot(email='email', password='password', prefix="/")


@bot.on_ready
async def on_ready():
    logger.info('Ready.')


@bot.command('ping')
async def echo(ctx: Context):
    await ctx.reply('Pong!')


if __name__ == '__main__':
    bot.start()
```
![](https://media.discordapp.net/attachments/868188677602422804/931159730393591870/anim.gif)

If you have any problems, please write to this discord https://discord.gg/SfzWs5djpT
