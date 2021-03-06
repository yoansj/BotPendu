##
## YOANSJ PROJECT, 2019
## PenduBot
## File description:
## bot
##

import tweepy
import os
import time
import consts
import pendu

#important keys to id the application
CONSUMER_KEY = 'YOURKEY'
CONSUMER_SECRET = 'YOURKEY'
ACCESS_KEY = 'YOURKEY'
ACCESS_SECRET = 'YOURKEY'

#auth to twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class TweetListener(tweepy.StreamListener):

    #Adds text into log file
    def add_log(self, text):
        f = open("logs.txt", "a+")
        localtime = time.asctime(time.localtime(time.time()))
        f.write(":" + localtime + " " + text + ":\n")
        print localtime, ": added", text, "in logs"
        f.close()

    #Updates the file of an existing game
    #Takes information in the tmp_player variable
    def update_file(self, name, tmp_player):
        f = open(consts.RUNNING_GAMES + name + ".txt", "w")
        tmp1 = "".join(tmp_player.to_find)
        tmp2 = "".join(tmp_player.user_word)
        f.writelines("HP " + str(tmp_player.u_hp) + "\n" +
        "TOFIND " + tmp1 + "\n" + tmp2 + "FOUND " + 
        str(tmp_player.letter_found))
        f.close()

    #Respond to the user
    #If the tweet is a game tweet
    def respond_game(self, tmp_player, status):
        tmp = "".join(tmp_player.user_word)
        TweetListener.add_log(self, "Responding game status to user " + status.user.screen_name)
        api.update_status("@" + status.user.screen_name + "\n" + pendu.print_hangman(tmp_player.u_hp) 
        + "\n" + tmp + "\n> Respond with your letters", status.id)

    #When we receive a tweet
    def on_status(self, status):
        print status.text, "Processing tweet..."
        api.create_favorite(status.id)
        TweetListener.add_log(self, status.text)
    #If we found a tweet containing only a mention
    #We stop processing the tweet
        tmp = status.text.split()
        if len(tmp) <= 1:
            TweetListener.add_log(self, "Bad tweet end of processing")
            api.destroy_favorite(status.id)
            return
    #If we find a command then we stop processing the tweet
    #We print a message and destorys the favorite
        if TweetListener.search_command(self, status) == consts.RETURN_NO_ERROR:
            api.destroy_favorite(status.id)
            print "Tweet processed, command found"
            return
    #If we cant fill the class from the file it means that the user has no game started
    #If that happens we stop processing the command and send a tweet to the user
        global tmp_player
        if tmp_player.fill_class_from_file(status.user.screen_name, status.text) == consts.RETURN_ERROR:
            api.update_status("@" + status.user.screen_name + "\n" + "You have no game running\n" +
            "If you want to play use " + consts.COMMAND_START + "\nIf you want some help use " + consts.COMMAND_HELP,
            status.id)
            api.destroy_favorite(status.id)
            return
        tmp_player = pendu.search_letter(tmp_player)
        TweetListener.update_file(self, status.user.screen_name, tmp_player)
        TweetListener.respond_game(self, tmp_player, status)
        api.destroy_favorite(status.id)


    #def end_condition(self, status, tmp_player):
    #    if tmp_player.u_hp <= 0:
            
    #Checks if a game is running
    #If a game is running responds with an error message
    #Otherwise creates a file for the player and then tweets
    def create_game(self, status):
        f = os.path.isfile(consts.RUNNING_GAMES + status.user.screen_name + ".txt")
        if f:
            TweetListener.add_log(self, consts.LOG_GAME_RUNNING + status.user.screen_name)
            api.update_status("@" + status.user.screen_name + "\n" + consts.TWEET_ERROR_GAME_RUNNING, status.id)
            return
        else:
            f = open(consts.RUNNING_GAMES + status.user.screen_name + ".txt", "a+")
            TweetListener.add_log(self, consts.LOG_CREATING_GAME + status.user.screen_name)
            chosen_word = pendu.randword()
            f.writelines("HP 8\n" + "TOFIND " + chosen_word + pendu.fill_user_word(chosen_word) + "\nFOUND 0")
            api.update_status("@" + status.user.screen_name + "\n" + pendu.print_hangman(8) 
            + "\n" + pendu.fill_user_word(chosen_word) + "\n> Respond with your letters", status.id)            


    #Checks if a game is running
    #If a game is running stops it by removing the file
    #If not responds to the user with an error message
    def quit_game(self, status):
        f = os.path.isfile(consts.RUNNING_GAMES + status.user.screen_name + ".txt")
        if f:
            os.remove(consts.RUNNING_GAMES + status.user.screen_name + ".txt")
            TweetListener.add_log(self, consts.LOG_GAME_STOPPED + status.user.screen_name)
            api.update_status("@" + status.user.screen_name + "\n" + consts.TWEET_GAME_STOPPED, status.id)
            return
        else:
            TweetListener.add_log(self, consts.LOG_GAME_STOPPED_FAIL + status.user.screen_name)
            api.update_status("@" + status.user.screen_name + "\n" + consts.TWEET_GAME_STOPPED_FAIL, status.id)


    #Searches for a command inside a tweet
    #If a command is found executes it and returns ok
    def search_command(self, status):
        tab = status.text.lower().split()
        for ta in tab:
            if ta == consts.COMMAND_START:
                TweetListener.create_game(self, status)
                return consts.RETURN_NO_ERROR
            if ta == consts.COMMAND_QUIT:
                TweetListener.quit_game(self, status)
                return consts.RETURN_NO_ERROR

    #If we receive an error what do we do
    def on_error(self, status):
        if status == 420:
            print "Slowing down..."
            return False
        print(status)

#launching the bot
tmp_player = pendu.player()
bot = TweetListener()
bot = tweepy.Stream(auth = api.auth, listener=bot)
bot.filter(track=['YOURTRACK'])