##
## YOANSJ PROJECT, 2019
## PenduBot
## File description:
## pendu
##

from random import *
import consts
import image
import os

#Returns a random word from the words list
def randword():
    f = open("words.txt", "r")
    lines = f.readlines()
    new = lines[randint(0, len(lines)-1)]
    f.close()
    return new.upper()

#Fills user word with ? equal to len of word to be found - 1
def fill_user_word(word):
    new = ""
    i = 0
    while i != len(word) - 1:
        new = new + "?"
        i += 1
    return new

#Prints the hangman
def print_hangman(hp):
        if hp <= 0:
            print "---PERDU---"
            print image.pendu[7]
            return image.pendu[7]
        if hp != 0:
            print "---VIES---"
        else:
            print "---PERDU---"
        print image.pendu[8-hp]
        return image.pendu[8-hp]

#Function that calls itself recursively to check if the letter entered...
#...by the user is located multiple times in to_find word
def find_same_letter(i, pinfo):
    tmp = pinfo
    find_result = "".join(tmp.to_find).find(tmp.u_input[i].upper())
    if (find_result != -1):
        tmp.user_word[find_result] = tmp.to_find[find_result]
        tmp.to_find[find_result] = "*"
        print tmp.user_word[find_result], tmp.to_find[find_result]
        tmp.letter_found = tmp.letter_found + 1
        tmp = find_same_letter(i, tmp)
    return tmp

#Searches for all the letters entered by the user if they are in the to_found word
#If a letter isnt in to_found then player looses one hp
def search_letter(pinfo):
    tmp = pinfo
    input_len = len(tmp.u_input)
    i = 0
    find_result = 0
    while i != input_len:
        find_result = "".join(tmp.to_find).find(tmp.u_input[i].upper())
        if (find_result == -1):
            tmp.u_hp -= 1
            print "Mauvaise lettre :(", tmp.u_input[i]
        else:
            tmp.user_word[find_result] = tmp.to_find[find_result]
            tmp.to_find[find_result] = "*"
            tmp.letter_found = tmp.letter_found + 1
            tmp = find_same_letter(i, tmp)
        i += 1 
    return tmp
    
class player():

    u_hp = 8
    letter_found = 0
    u_input = ""
    to_find = list(randword())
    objective = to_find.__len__() - 1
    user_word = list(fill_user_word(to_find))

    def fill_class_from_file(self, file):
        f = os.path.isfile(consts.RUNNING_GAMES + file + ".txt")
        if f:
            print "Found file of player", file
        else:
            print "Error no file found, responding with an error tweet"
            return consts.RETURN_ERROR
        f = open(consts.RUNNING_GAMES + file + ".txt", "r")
        content = f.readlines()
        for line in content:
            if "HP" in line:
                tmp = line.split()
                self.u_hp = int(tmp[1])
            if "FOUND" in line:
                tmp = line.split()
                self.letter_found = int(tmp[1])
            if line[0] == "?":
                self.user_word = line
            if "TOFIND" in line:
                tmp = line.split()
                self.to_find = tmp[1]
            

def gameloop():
    pinfo = player()
    print "".join(pinfo.to_find)
    print_hangman(pinfo.u_hp)
    while pinfo.letter_found != pinfo.objective and pinfo.u_hp > 0:
        #print "[DEBUG][HP:", pinfo.u_hp, "]", "[LF:", pinfo.letter_found, "]", pinfo.letter_found, pinfo.objective
        print ">", "".join(pinfo.user_word)
        pinfo.u_input = raw_input("Entrez vos lettres: ")
        pinfo = search_letter(pinfo)
        print_hangman(pinfo.u_hp)
