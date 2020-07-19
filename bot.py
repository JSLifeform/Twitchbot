#This will be the bot script

import os # for importing env vars for the bot to use
from twitchio.ext import commands # library which allows @bot.event and command classes/functions
from dice import Die, D6 #imports dice objects
from threes_game import Hand, threes_low, check_int #imports a couple functions I was too lazy to retype

# variable to store hand and corresponding players
dice_players = {}

def print_hand(ctx, hand):
    'Creates string showing values of dice and whic are kept'
    player = ctx.author.name.lower()
    show_hand = (f"{player}'s dice are:  ")
    for dice in hand:
        if dice.locked == True:
            show_hand += (str(dice.value) + '-KEPT    ')
        else:        
            show_hand += (str(dice.value) + '  ')
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

    #listens for Twitch commands
    await bot.handle_commands(ctx)
    # prints chat text to console
    print(ctx.content)

@bot.command(name = 'giveup')
async def give_up(ctx):
    'Clears player from game queue and sends an encouraging video'
    try:
        del dice_players[ctx.author.name.lower()]
    except KeyError:
        await ctx.send(f"{ctx.author.name.lower()}, you don't appear to be in the game yet!")
    else:
        await ctx.send('Giving up alread? Remember folks, be like Rick! https://www.youtube.com/watch?v=dQw4w9WgXcQ')

@bot.command(name = 'dice')
async def dice(ctx):
    'command used to interact with dice game'
    # allows for shorter typing of this obnoxious string for player name calls
    name = ctx.author.name.lower()

    if name in dice_players:
        # pulls number off dice command for kept dice
        response = ctx.content.split(' ', 2)
        
        # checks that response is integer, warns chat if not an integer given
        try:
            response = int(response[1])
        except ValueError:
            await ctx.channel.send('''You did not appear to enter a valid amount of dice to be kept...
             Make sure you follow the "!Dice *" format.''')
        else:
            if response + dice_players[name][5] > 5:
                await ctx.channel.send(f'Too many dice to keep, currently {dice_players[name][5]} out of 5 kept')
                return
            # adds to total of kept dice for player
            dice_players[name][5] += response


            # locks dice that are kept each round
            for i in range(dice_players[name][5]):
                #locks kept dice and prints score of kept dice in command prompt
                dice_players[name][i].locked = True
                print(f'Die #{i + 1} locked with score of {dice_players[name][i].score}')

            #refreshes unkept dice if less than 5 kept
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
                output = f'{ctx.author.name.lower()}' + ''',  how many dice would you like to keep this round? 
    Enter the number of dice you want to keep after the !dice command: i.e. enter "!dice 2" if you 
    want to keep 2 dice, You must keep at least 1 die each round'''
                await ctx.send(output)

            # initiates game end sequence if all dice are kept
            else:
                score = dice_players[name].pop()
                keepers = dice_players[name].pop()
                for dice in dice_players[name]:
                    score += dice.score
                
                # adds kept dice to string to display to user in game over message
                final_hand = ''
                for die in dice_players[name]:
                    final_hand += (str(die.value) + ' ')

                #shows game ending message and stats    
                await ctx.send(f'''Congratulations {name}, your game has ended! You scored {score} points!
                 Your final hand was: {final_hand}''')

                # cleans up variables, are score and keepers unnecessary since they only exist in a loop?
                del dice_players[name], score, keepers, final_hand
           
    #if player not in dictionary, initiates dice game, creates hand
    else:
        await ctx.send(f'Initiating dice game with {ctx.author.name.lower()}')
        h = Hand()
    # adds user to listof active players
        player = ctx.author.name.lower()
        print(player)
        roll = Hand()

        # list to make new dice hands
        hand = []
        #adds dice to hand
        for dice in roll:
            hand.append(dice)
        #adds 0's to player dictionary, indicating starting score of 0 and 0 kept dice respectively
        dice_players[player] = hand + [0, 0]
        await ctx.send(print_hand(ctx, hand))


if __name__ == "__main__":
    bot.run()