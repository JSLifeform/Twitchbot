# MTGNerdBot

Thank you for using my MTGNerdbot! The original plan was to create a bot that streamers playing Magic: The Gathering would using, but so far I have been unable to get a streamer to give me a realistic request for a chat bot feature I can code. So, instead I made one that lets you play a dice game in Twitch chat! The game is called "Threes," or "Threes Low." It is a dice game which I will describe in detail below.


Acknowledgments: Thanks to all the Code Louisville team over the past 2 years for pushing me to learn a new skill and hopefully further my career!




## CODE LOUISVILLE PROJECT REQUIREMENTS

Requirements met for the May 2020 Code Louisville Python project are as follows:

*  Implement a “master loop” console application where the user can repeatedly enter commands/perform actions, including choosing to exit the program
*  Create a dictionary or list, populate it with several values, retrieve at least one value, and use it in your program
*  Connect to an external/3rd party API and read data into your app
*  Build a conversion tool that converts user input to another type and displays it (ex: converts cups to grams) (I think? I convert the string input from the API into an integer to use in my program)
*  Potentially others I forgot about! I'm quite confident I hit the minimum requirements already and am too lazy to try to pick out other requirements I randomly satisfied in my endeavor




## HOW TO RUN

This project was created with pipenv. The pipfile and pipfile.lock files are included in the repo. The dependencies can be installed through the command "pip install" within the project folder. The user must also create a .env file (simply named ".env", where the env is the file extension - no actual file name is wanted) where they include the name of their channel, bot, client ID and oauth token to access the Twitch API (NOTE: Code Louisville mentor -  contact me on slack "John Locken" and I can DM you my .env file. You can simply copy/paste the text from my .env file into yours). Afterwards, you can set up the virtual environment with the "pipenv install" command. Once you've done this, you should be able to run the program with "pipenv run python bot.py". After that, the bot should be online at https://www.twitch.tv/mtgnerdbot. You can interact with it within the Twitch chat at that page. NOTE: A Twitch username must be created in order to use Twitch chat.


### HOW TO RUN, ABRIDGED

* download project to local machine
* navigate to project folder in command prompt
* Create .env file <---------- data for .env file can be sent via Slack from John Locken
* run "pip install pipenv" <------This will install pipenv on your machine, only necessary if not installed already
* run "pipenv install" <---------- This will install required packages in project virtual envrionment
* run "pipenv run python bot.py" <-------This will start the bot
* interact with bot at https://www.twitch.tv/mtgnerdbot. Click on chat to open the chat menu.
* have fun rolling dice!




## THE BOT

The chat bot currently has one main function: to allow user to play the Three's dice game in chat


### Bot Limitations

The glaring limitation with the bot currently is that all game actions must be used through the main Twitch chat using the "!dice" command. The key issue with this is that if a player wants to perform the same game action (such as "!dice 1") they must wait 30 seconds between actions. This is due to a Twitch chat feature that will not allow a person to post the same chat message twice in a 30 second period. Hopefully this will be fixed by using the whisper feature in future versions, but the Twitchio library used in this bot does not currently work using the Twitch whisper feature.





## THREE'S

Three's, or "Three's Low," is a dice game typically played with 5 six-sided dice. The goal of the game is to get the lowest score possible. The player rolls all 5 dice at the start of the game. Once the dice have been rolled, the player chooses one or more dice to "keep." These dice will not be rerolled and will be added to the final score. Once the player has picked a number of dice to keep, they will reroll the remaining dice. The player must then choose to keep one or more of the rerolled dice, adding it to the final score. This process is continued until all dice are kept.

### Scoring

A player's final score is equal to the sum of the face value of all kept dice with one exception: any dice showing a 3 on it's face is scored as 0. For example, a final kept hand of 3 3 1 4 5 will be scored as a 10. A perfect game is a hand of all 3's, yielding a score of 0.




### HOW TO PLAY

(Note: you must have a Twitch username in order to interact with Twitch chat) Initiate a game by typing "!dice" into the Twitch chat where the bot is initialized. This will intialize a game and roll a starting hand for the player. After the results are displayed, type "!dice *" into chat, where * is the number of dice you want to keep (EXAMPLE: "!dice 2" will keep 2 dice). The game automates to keep the lowest scoring dice, so no need to pick which individual dice to keep! Once you have kept your dice, the bot will reroll the rest and show you your hand, with "-KEPT" proceeding all the dice you've already locked in. Repeat this process until all dice are kept, then the bot will display a final score! You will be automatically removed from the game database so you may restart another game by typing "!dice" again. You may also type "!giveup" into the chat at any time to cancel the current game.

#### HOW TO PLAY, ABRIDGED

* type "!dice" in chat to start game
* type "!dice (num_dice)" to choose how many dice to keep this round (e.g "!dice 2" for 2 dice)
* game will automatically terminate after all dice are kept, score will be displayed
* type "!giveup" at any time to stop the game and purge the player from the queue




## QUITTING THE BOT

As of right now, the only way to quit the bot is to use the hotkey quit (ctrl + c in Windows) or to close the cmd window it is running in. This may be changed in future versions but I'm not sure of a good way to do that without adding a Twitch command, which has to omuch potential for abuse.



## Conclusion

Thank you for taking the time to look at my project, any feedback is appreciated! A lot more time than I'm willing to admit has gone into the paltry coding skills I've earned so far, and I'm always looking for criticism to help me improve... or accolades to inflate my ego :smiling_face_with_three_hearts: Thank you again for your interest in my project, and until our paths cross again, cheers! :beers: :beers: :beers: