#This will be the bot script
import os # for importing env vars for the bot to use
from twitchio.ext import commands
from dice import Die, D6 
from threes_game import Hand, threes_low, check_int

# variable to store hand and corresponding players
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
    # prints chat text to console
    print(ctx.content)

@bot.command(name = 'dice')
async def dice(ctx):
    if ctx.author.name.lower() in dice_players:
        # pulls number off dice command for kept dice
        response = ctx.content.split(' ', 2)
        # checks that response is integer, warns chat if not an integer given
        try:
            response = int(response[1])
        except ValueError:
            await ctx.channel.send('''You did not appear to enter a valid amount of dice to be kept> Make sure you
            follow the "!Dice 2" format.''')
        else:
            if response + dice_players[ctx.author.name.lower()][5] > 5:
                await ctx.channel.send(f'Too many dice kept, currently {dice_players[ctx.author.name.lower()][5]} out of 5 kept')
                return
            dice_players[ctx.author.name.lower()][5] += response
            print(dice_players[ctx.author.name.lower()][5])
            print(dice_players[ctx.author.name.lower()])
            #for dice in dice_players[ctx.author.name.lower()] in range (0, int(dice_players[ctx.author.name.lower()][5])):
             #   dice.locked = True
        # await ctx.channel.send(response[1])
    else:
        #initiates dice game, creates hand
        await ctx.send(f'Initiating dice game with {ctx.author.name.lower()}')
        h = Hand()
    # adds user to list, hopefully to coordinate dice game with active players
        player = ctx.author.name.lower()
        print(player)
        roll = Hand()
        # list to make new dice hands
        hand = []
        for dice in roll:
            hand.append(dice)
        print(hand)
        dice_players[player] = hand + [0, 0]
        await ctx.send(f'{player}s dice are:')
        show_hand = ''
        for dice in hand:
            if dice.locked == True:
                show_hand += (str(dice.value) + ' KEPT ')
            else:        
                show_hand += (str(dice.value) + '   ')
        await ctx.send(show_hand)


    output = f'{ctx.author.name.lower()}' + ''',  how many dice would you like to keep this round? Enter the
    number of dice you want to keep after the !dice command: i.e. enter "!dice 2" if you want to keep 2 dice
    You must keep at least 1 die each round'''
    await ctx.send(output)




if __name__ == "__main__":
    bot.run()