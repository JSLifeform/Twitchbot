#This will be the bot script
import os # for importing env vars for the bot to use
from twitchio.ext import commands
from dice import Die, D6 
from threes_game import Hand, threes_low, check_int

dice_players = {}

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")

    # bot.py, below event_ready
@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    #bot.py, in event_message, below the bot ignore stuffs
    #listens for !dice command
    await bot.handle_commands(ctx)
    #says 'yo' to anyone who chats
    await ctx.channel.send('yo')
    print(ctx.content)

@bot.command(name = 'dice')
async def dice(ctx):
    if ctx.author.name.lower() in dice_players:
        await ctx.channel.send('you in brah!')
    else:
        await ctx.send(f'Initiating dice game with {ctx.author.name.lower()}')
    # adds user to list, hopefully to coordinate dice game with active players
        player = ctx.author.name.lower()
        print(player)
        add_player = {}
        dice_players.update(player = Hand())
    # prints list of users for testing purposes
    print(dice_players)

    # testing to see dice values
    h = Hand()
    for dice in h:
        print(dice.value)



if __name__ == "__main__":
    bot.run()