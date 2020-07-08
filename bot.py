#This will be the bot script
import os # for importing env vars for the bot to use
from twitchio.ext import commands
from dice import Die, D6 
from threes_game import Hand, threes_low, check_int

# variable to store hand and corresponding players
dice_players = {}

def print_hand(ctx, hand):
    player = ctx.author.name.lower()
    show_hand = (f'{player}s dice are:            ')
    for dice in hand:
        if dice.locked == True:
            show_hand += (str(dice.value) + '-KEPT    ')
        else:        
            show_hand += (str(dice.value) + '      ')
    return show_hand



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
    # allows for shorter typing of this obnoxious string for name calls
    name = ctx.author.name.lower()
    if name in dice_players:
        # pulls number off dice command for kept dice
        response = ctx.content.split(' ', 2)
        # checks that response is integer, warns chat if not an integer given
        try:
            response = int(response[1])
        except ValueError:
            await ctx.channel.send('''You did not appear to enter a valid amount of dice to be kept...
             Make sure you follow the "!Dice 2" format.''')
        else:
            if response + dice_players[name][5] > 5:
                await ctx.channel.send(f'Too many dice to keep, currently {dice_players[name][5]} out of 5 kept')
                return
            dice_players[name][5] += response
            print(dice_players[name][5])
            print(dice_players[name])
            # for dice in dice_players[ctx.author.name.lower()] in range (0, int(dice_players[ctx.author.name.lower()][5])):
            # locks dice that are kept each round
            for i in range(dice_players[name][5]):
                dice_players[name][i].locked = True
                print(f'Die #{i} locked with score of {dice_players[name][i].score}')
            # for dice in dice_players[ctx.author.name.lower()] in range(5): <--- deprecated delete?
            #     if dice.locked == True:   <--- deprecated delete?
            #         print("locked!")    <--- deprecated delete?

            #refreshes dice if less than 5 kept
            if dice_players[name][5] < 5:
                score = dice_players[name].pop()
                keepers = dice_players[name].pop()
                print(keepers)

                # re-rolls unkept dice
                for i in range(keepers, 5):
                    dice_players[name][i] = D6()
                # re-sorts hand based on threes being lowest number
                dice_players[name].sort(key = threes_low)
                #sends dice hand BEFORE appending keepers and score to player dictionary list
                await ctx.send(print_hand(ctx, dice_players[name]))
                
                #appends keepers and score to player dictionary
                dice_players[name].append(keepers)
                dice_players[name].append(score)
                print(dice_players[name])
            else:
                score = dice_players[name].pop()
                keepers = dice_players[name].pop()
                for dice in dice_players[name]:
                    score += dice.score
                print(score)
                await ctx.send(f'''Congratulations {name}, your game has ended! You scored {score} points!
                 If it's not a Goose Egg then you're nothing!''')
                # cleans up variables, are score and keepers unnecessary since they only exist in a loop?
                del dice_players[name], score, keepers
   
            #this has to be the Python-y way to do it, above is clunky
            #for dice in dice_players[ctx.author.name.lower()]:
                #print(dice)
                
                #for dice in range(0, int(ctx.author.name.lower()[5])):
                   # dice.locked = True
                   # print(dice.locked)
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
        await ctx.send(print_hand(ctx, hand))

        # below 6 now in print_hand(), deprecated, delete?
        # for dice in hand:
        #     if dice.locked == True:
        #         show_hand += (str(dice.value) + ' KEPT ')
        #     else:        
        #         show_hand += (str(dice.value) + '   ')
        # await ctx.send(show_hand)


    output = f'{ctx.author.name.lower()}' + ''',  how many dice would you like to keep this round? 
    Enter the number of dice you want to keep after the !dice command: i.e. enter "!dice 2" if you 
    want to keep 2 dice, You must keep at least 1 die each round'''
    await ctx.send(output)

    print(dice_players)



if __name__ == "__main__":
    bot.run()