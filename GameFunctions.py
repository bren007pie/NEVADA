#This is the file used for most backend, interaction, startup/global variables,  functions of the game


from GameClasses import *
import StartUp
import AsciiArt
import time
import os  # used to put files in the cache folder
from printT import * #import it all
import colorama  # Colour module, no bolding on windows :(
from colorama import Fore, Back, Style

colorama.init()
CLEARSCREEN = '\033[2J'  # This is the clearscreen variable
lightgreen = Fore.LIGHTGREEN_EX


# This is where the global variables are instantiated and defined. Global variables used to pass info between functions
# TODO will be changed to pass by reference) and dictionaries used to store many variables/objects in one
#   place while making it clear in the code which one is being referenced

MAPS = StartUp.WorldMap() 
ITEMS = StartUp.ItemDictionary()
ENEMIES = StartUp.EnemyDictionary()
INTERACT = StartUp.InteractDictionary()
INTERIORS = ["OverWorld","BSB","Capstone Room"]  # List of interior names with the index location being the dimension/building number
# ex) 0 is OverwWord, 1 is BSB, 2 is capstone room, etc




GAMEINFO = {'version':0,'versionname':"", 'releasedate':"",'playername':" ",'gamestart':0,'timestart':0,
            'runtime': 0, 'stepcount':0,'commandcount':0,'log': [],"layersdeep":0,"savepath": "","help": ""}
#this dictionary is used to store misc game info to be passed between function:
# speedrun time, start time, etc. Values are initialized to their value types
# version is version of the game, gamestart is the first start time of the game, runtime is the total second count,
# log is log of all player input, layers deep is how many layers deep in the laptop quest you are, help is help prinout,

GAMEINFO['help'] = "(\S)The complexities of reality have been distilled into 4 things (~Places~, <objects>, /interacts/, and [people]) " \
                   "(\S) (\S)These are the commands your brain can handle in this state:" \
                   "(\S)(l,r,f,b,u,d)go left/right/front/back/up/down (you can't turn)" \
                   "(\S)(e)equip objects" \
                   "(\S)(dr)drop objects" \
                   "(\S)(exa)examine objects" \
                   "(\S)(ea)eat objects" \
                   "(\S)(i)inventory (check inventory)" \
                   "(\S)(exa)examine interacts (uses an item when you have the right thing) " \
                   "(\S)(us)use objects (use an item on a nearby interact)" \
                   "(\S)(t)talk person  (gives them an item when you have the right thing)" \
                   "(\S)(g)give object (gives an object to a person around you)" \
                   "(\S)(a)attack person (Force may be necessary but be careful, you're limited by what you have)" \
                   "(\S)(s)search (look at what's around you)" \
                   "(\S)(r)remember (remember what you were doing here earlier)" \
                   "(\S)exit (exit your body)" \
                   "(\S)shortcuts (gives shortcuts list)" \
                   "(\S)(h)help (gives you this list again)" \
                   "(\S) (\S)While you may accept more commands that is up to you to discover."



QUESTS = {}  #initializing the quests global variable to be later writen into

GAMESETTINGS = {'DisableOpening': 0, 'SpeedRun': 0, 'HardcoreMode':0, 'DevMode': 0, 'loadgame':0}
# disable openning, speedrun disables openning;lore read times; might disable secrets or opens them,
# hardcore for now disables eating but might make enemies harder,
# DevMode disables the main error catching + Startup Blip
# loadgame is a flag for loading to skip the setup

STARTLOCATION = (2,3,1,0)
STARTHEALTH = 100


EMPTYHEAD = Equipment('EMPTY',(None,None,None),'EMPTY.png','Nothing is Equipped','head',(0,0,0),-101)
EMPTYBODY = Equipment('EMPTY',(None,None,None),'EMPTY.png','Nothing is Equipped','body',(0,0,0),-101)
EMPTYHAND = Equipment('EMPTY',(None,None,None),'EMPTY.png','Nothing is Equipped','hand',(0,0,0),-101)
EMPTYOFFHAND = Equipment('EMPTY',(None,None,None),'EMPTY.png','Nothing is Equipped','off-hand',(0,0,0),-101)
EMPTYINV = {'head':EMPTYHEAD,'body':EMPTYBODY,'hand':EMPTYHAND,'off-hand':EMPTYOFFHAND}
STARTINV = {'head':EMPTYHEAD,'body':EMPTYBODY,'hand':EMPTYHAND,'off-hand':EMPTYOFFHAND}
#STARTINV = {'head':ITEMS['gas mask'],'body':ITEMS['okons chainmail'],'hand':ITEMS['iron ring'],'off-hand':ITEMS['green bang bong']}

# OBJECTS need to be UNIQUE so that the location doesn't get messed up when duplicate objects in the game
TYINV = {'head':ITEMS["tyler's visor glasses"],'body':ITEMS["tyler's big hits shirt"],'hand':ITEMS["tyler's hulk hands"],'off-hand':ITEMS["tyler's green bang bong"]} #gets to have the Iron Ring when he graduates


# TODO Make PLAYER into PLAYERS a dictionary of playable characters objects
PLAYER = Character('Minnick',list(STARTLOCATION),STARTHEALTH,STARTINV,EMPTYINV)
Tyler = Character('Tyler Kashak',list(STARTLOCATION),999,TYINV,EMPTYINV)
# MAPS[6][1][1][0].placeItem(ITEMS["big hits shirt"]) #having these spawn the items in the map after should get rid of the wierd bug from having Tyler Kashak having them to start
# MAPS[0][3][0][0].placeItem(ITEMS["hulk hands"])

# Setting up the game path for the game to the cache folder
# Using os here to get the current file path and the os.path.join to add the // or \ depending on if it's windows or linuix
# joining an empty string just gives a slash
GAMEINFO['savepath'] = os.path.join(os.getcwd(), "cache","")

try:
    os.makedirs(GAMEINFO['savepath'])  # gets the directory then makes the path if it's not there
    # CAN"T have last \ in the file path so have to use [:-1] to use all string but the last character
    # Not hiding individual files so can access and also will throw an error to access if files are hidden
    os.system("attrib +h " + GAMEINFO['savepath'][:-1])  # Makes cache file hidden

except:
    print "\n"  # does nothing if the path is already there


# TODO Make these functions into class methods related to each class
def Equip(Item):
    global PLAYER
    global ITEMS
    global MAPS
    global INTERACT
    x = PLAYER.location[0]
    y = PLAYER.location[1]
    z = PLAYER.location[2]
    dim = PLAYER.location[3]
    Place = MAPS[x][y][z][dim]
    if Item in ITEMS:  # if name of Item asked for in parser is in ITEMS dictionary
        # this is different than the equip method in the Character class.
        # Makes sure the item is dropped at the current location
        drop = PLAYER.equip(ITEMS[Item])
        Place.removeItem(ITEMS[Item])
        Place.placeItem(drop)

        
    elif Item in INTERACT and list(INTERACT[Item].location) == PLAYER.location:
        printT("Maybe if you were at your peak you could carry a " + str(INTERACT[Item].name) + " but not with this migraine.")
    elif Item in ENEMIES and list(ENEMIES[Item].location) == PLAYER.location and ENEMIES[Item].alive:
        printT("You attempt to pick up " + ENEMIES[Item].name + " but you're not that close... (\S)And now you're both really uncomfortable.")
    elif Item in ENEMIES and list(ENEMIES[Item].location) == PLAYER.location and not ENEMIES[Item].alive:
        printT("That's pretty messed up. You probably shouldn't pick up " + ENEMIES[Item].name + "'s body.")
    else:
        print "\nYou can't find that around here. Maybe it's your hungover typing."


def Drop(Item):
    global MAPS
    global PLAYER
    global ITEMS
    global ENEMIES
    x = PLAYER.location[0]
    y = PLAYER.location[1]
    z = PLAYER.location[2]
    dim = PLAYER.location[3]
    Place = MAPS[x][y][z][dim]
    if Item in ITEMS:
        drop = PLAYER.drop(ITEMS[Item])
        Place.placeItem(drop)
        # Same as equip function. 'None' passed to function if item doesn't exist
    elif Item in ENEMIES and list(ENEMIES[Item].location) == PLAYER.location and ENEMIES[Item].alive:
        printT("You drop " + ENEMIES[Item].name + " but they were never yours to begin with. (\S)Now you just have one less friend..")
    else:
       printT("Maybe you're still drunk?. You aren't carrying " + Item + ".")



def Move(direction):
    global MAPS
    global PLAYER
    global ENEMIES
    global INTERACT
    global ITEMS
    bf = ENEMIES['brendan fallon']
    x = PLAYER.location[0]
    y = PLAYER.location[1]
    z = PLAYER.location[2]
    dim = PLAYER.location[3]
    currentplace = MAPS[x][y][z][dim]  # Saving your current map location to a variable
    place = 0
    # TODO Bugfix, walls only registers for single letter movements not full commands, another reason to make transforms
    if direction not in currentplace.walls:
        # TODO Make these direction additions transformations (matrix transforms)
        # These are the direction parsing
        if direction in ['f','forward', 'ahead', 'w', 'west']:
            y += 1
        elif direction in ['b','back', 'backward', 'e', 'east']:
            y -= 1
        elif direction in ['r','right','n','north']:
            x += 1
        elif direction in ['l','left', 's', 'south']:
            x -= 1
        elif direction in ['u','up']:
            z += 1
        elif direction in ['d','down']:
            z -= 1
        else:
            print "You stumble over not sure where you were trying to go. You brain doesn't understand " + direction
            return
        # TODO This is where links come in which direct into interriors

        place = MAPS[x][y][z][dim]  # place is new location requested

        #  INTERRIORS DISABLED FOR NOW
        # # Interrior Links: If the spot has a link might be teliported/moved to that place
        # for link in currentplace.links:  # if there is links in it it will loop through
        #     if direction in link:  # Searching all the links to see if any links refer to that direction
        #         if dim == 0 and link[4] != 0:
        #             print "You go inside " + INTERIORS[link[4]] + "."  # When going to non-Overworld it says going inside
        #         elif dim != 0 and link[4] == 0: # When going to overworld from non
        #             print "You go outside."
        #         elif dim != link[4]:  # Leaving one interior and entering another
        #             print "You leave " + INTERIORS[dim] + " and enter " + INTERIORS[link[4]] + "."
        #
        #         x = link[1]
        #         y = link[2]
        #         z = link[3]
        #         dim = link[4]
        #         place = MAPS[x][y][z][dim]  # Overwrites place with the link location


    if place:
        PLAYER.location[0] = x
        PLAYER.location[1] = y
        PLAYER.location[2] = z
        PLAYER.location[3] = dim

        if bf.location != (None,None,None,None):
            MAPS[bf.location[0]][bf.location[1]][bf.location[2]][bf.location[3]].removeEnemy(bf)
        if random() <= 0.003: 
            MAPS[x][y][z][dim].placeEnemy(bf)
            # AsciiArt.Hero()  # TODO Enable once Dynamic Ascii Art
            
        if place.travelled:  # This is the printout section for each time you move
            print "You enter " + Back.WHITE + Fore.BLACK +  place.name + Back.RESET + lightgreen + "\n"
            printT(place.lore)
            printT("(\S)" + Back.WHITE + Fore.BLACK + "~"+place.name.upper() + "~ (\S)" + Back.RESET + lightgreen + place.search(MAPS),72,0.75)  # (\S) used for printT newline
            place.travelled = 0
        else:  # If returning to the place
            printT("(\S)" + Back.WHITE + Fore.BLACK + "~"+place.name.upper() + "~ (\S)" + Back.RESET + lightgreen + place.search(MAPS),72,0.25)  # (\S) used for printT newline
            return place
            
        
    else:
        PLAYER.location[0] = currentplace.location[0]
        PLAYER.location[1] = currentplace.location[1]
        PLAYER.location[2] = currentplace.location[2]
        PLAYER.location[3] = currentplace.location[3]
        print "\nYou can't go that way!\n"
        return currentplace

#Combat System

def Combat(P,E):
     if E:      
        #Speed
        PSpeed = P.stats[2]
        ESpeed = E.stats[2]
        
        #Determine who goes first
        if PSpeed>ESpeed:
            First = P
            Second = E
        elif PSpeed<ESpeed:
            First = E
            Second = P
        else:
            Combatants = [E,P]
            First = choice(Combatants)
            Combatants.remove(First)
            Second = Combatants[0]   
        #Max damage each can deal
        FDamage = abs(First.stats[0])*First.stats[0]/(Second.stats[1]+1)
        SDamage = abs(Second.stats[0])*Second.stats[0]/(First.stats[1]+1)
        #Starting health
        FSHealth = First.health
        SSHealth = Second.health
        while (P.health and E.health):
            if First.health:
                Damage = int(uniform(0.7, 1)*FDamage)
                Second.health = max(0,Second.health - Damage)
            
            if Second.health:
                Damage = int(uniform(0.7, 1)*SDamage)
                First.health = max(0,First.health - Damage)
     # TODO Re-implement combat and number with word ques instead of numbers
     # if First == P:
     #     print "\nYou attack dealing " + str(SSHealth - Second.health) + " damage.\n" + Second.name + " deals " + str(FSHealth - First.health) + " damage.\n"
     #     print  "You have " + str(First.health) + " health remaining.\n" + Second.name + " has " + str(Second.health) + " health remaining.\n"
     # else:
     #     print "\n"+First.name + " dealt " + str(SSHealth - Second.health) + " damage.\n" + "You attack dealing " + str(FSHealth - First.health) + " damage.\n"
     #     print  "You have " + str(Second.health) + " health remaining.\n" + First.name + " has " + str(First.health) + " health remaining.\n"
     if P.health == 0:
        P.alive = False
        return 0
     if E.health == 0:
        E.alive = False
        return 1

def Attack(E):
    global ENEMIES
    global MAPS
    global PLAYER
    global ITEMS
    x = PLAYER.location[0]
    y = PLAYER.location[1]
    z = PLAYER.location[2]
    dim = PLAYER.location[3]
    CurrentPlace = MAPS[x][y][z][dim]
    if E in ENEMIES and (list(ENEMIES[E].location) == PLAYER.location) and (ENEMIES[E].alive):
        enemy = ENEMIES[E] #making it the object from the name
        bgchance = 0.01
        if PLAYER.inv['head'] == ITEMS['helm of orin bearclaw']:
            bgchance += 0.1 
        if PLAYER.inv['body'] == ITEMS['big hits shirt']:
            bgchance += 0.1
        if random() <= bgchance: #bigHits feature TODO have oblivion sound effects 
            # AsciiArt.BigHits()  # TODO Enable once Dynamic Ascii Art
            print "\nAn oblivion gate opens and a purple faced hero in ebony armour punches\n" + enemy.name + " to death."
            printT(enemy.Dinfo) #slow version
            enemy.alive = False
            if enemy.drop:
               print enemy.name + " dropped the " + ITEMS[enemy.drop].name + "."
               CurrentPlace.placeItem(ITEMS[enemy.drop])
        else:
           Outcome = Combat(PLAYER,enemy) 
           if Outcome:
               print "You defeated " + enemy.name + ".\n"
               printT(enemy.Dinfo)
               if enemy.drop:
                   print enemy.name + " dropped the " + ITEMS[enemy.drop].name + "."
                   CurrentPlace.placeItem(ITEMS[enemy.drop])
           else:
               print "Oh no! " + enemy.name + " defeated you!\nYou died, without ever finding your iron ring"
    else:
        print "\nThey don't appear to be here."
                        

def Talk(E):
    global ENEMIES
    global MAPS
    global PLAYER
    global ITEMS
    x = PLAYER.location[0]
    y = PLAYER.location[1]
    z = PLAYER.location[2]
    dim = PLAYER.location[3]
    if E in ENEMIES and ((list(ENEMIES[E].location) == PLAYER.location)) and (ENEMIES[E].alive):
        enemy = ENEMIES[E]
        if enemy.need and PLAYER.inv[ITEMS[enemy.need].worn]==ITEMS[enemy.need]and not enemy.quest:
            print enemy.name + " took the " + enemy.need + "."
            printT(enemy.Sinfo)  # default print speed
            ITEMS[enemy.need].location = (None, None, None)  # Brendan added this, used to clear the item location
            PLAYER.inv[ITEMS[enemy.need].worn] = PLAYER.emptyinv[ITEMS[enemy.need].worn]
            PLAYER.updateStats()
            enemy.quest = True
            if enemy.drop:
                MAPS[x][y][z][dim].placeItem(ITEMS[enemy.drop])
                print "You see a " + ITEMS[enemy.drop].name +".\n"
                enemy.drop = None      
        elif enemy.quest and enemy.drop:  # What is this for?

            printT(enemy.Sinfo)
            MAPS[x][y][z][dim].placeItem(ITEMS[enemy.drop])
            print "You see a " + ITEMS[enemy.drop].name +".\n"
            enemy.drop = None
        elif enemy.quest:
            printT(enemy.Sinfo)
        else:
            printT(enemy.info)
        enemy.spoke = True
        if GAMESETTINGS['DevMode']:  # If in devmode can see the stats/quest of enemies
            print "HEALTH: " + str(ENEMIES[E].health)
            print "ATK : " + str(ENEMIES[E].stats[0])
            print "DEF : " + str(ENEMIES[E].stats[1])
            print "SPD : " + str(ENEMIES[E].stats[2])
            print "NEED : " + str(ENEMIES[E].need)
            print "DROP : " + str(ENEMIES[E].drop)
            print "QUESTFlag : " + str(ENEMIES[E].quest)
            print "SPOKE : " + str(ENEMIES[E].spoke)


    elif E in ENEMIES and ((list(ENEMIES[E].location) == PLAYER.location)) and (ENEMIES[E].alive==False):
        print "\nI don't think they can do that anymore.\n"
    else:
        print "\nThey don't appear to be here.\n"

# TODO Re-implement stats and number with word ques instead of numbers
def Stats():
    global PLAYER
    print "\nHEALTH: " + str(PLAYER.health)
    print "ATK: " + str(PLAYER.stats[0])
    print "DEF: " + str(PLAYER.stats[1])
    print "SPD: " + str(PLAYER.stats[2])+"\n"

def Inspect(Item): #Item is the inspect item
    global MAPS
    global ITEMS
    global PLAYER
    global INTERACT
    x = PLAYER.location[0]
    y = PLAYER.location[1]
    z = PLAYER.location[2]
    dim = PLAYER.location[3]

    #If item in location
    if Item in ITEMS and list(ITEMS[Item].location) == PLAYER.location: #this is for item = equipment
        printT(ITEMS[Item].name.upper(),72,0)
        printT(ITEMS[Item].info,72,0)  # fast version for reading things
        # TODO re-implement inspecting item with words instead of numbers
        if GAMESETTINGS['DevMode']:  # If in devmode can see the stats
            print "ATK : " + str(ITEMS[Item].stats[0]) + " " + "("+str(ITEMS[Item].stats[0]-PLAYER.inv[ITEMS[Item].worn].stats[0])+")"
            print "DEF : " + str(ITEMS[Item].stats[1]) + " " + "("+str(ITEMS[Item].stats[1]-PLAYER.inv[ITEMS[Item].worn].stats[1])+")"
            print "SPD : " + str(ITEMS[Item].stats[2]) + " " + "("+str(ITEMS[Item].stats[2]-PLAYER.inv[ITEMS[Item].worn].stats[2])+")"
            print "WORN: " + str(ITEMS[Item].worn).upper()
            if ITEMS[Item].health: #if edible it shows that health stat plus what your final health would be if eaten
                print "Edible: Yes\n " #+ str(ITEMS[Item].health) + " (" + str(min(100,PLAYER.health + ITEMS[Item].health))+")" +"\n"
            else:
                print""
    # If the entered item is an intractable and is at that location
    elif Item in INTERACT and list(INTERACT[Item].location) == PLAYER.location: # this is for item = interactable
        if INTERACT[Item].need and PLAYER.inv[ITEMS[INTERACT[Item].need].worn]==ITEMS[INTERACT[Item].need]: #if you have the item the interactable needs worn on your body
            
            PLAYER.inv[ITEMS[INTERACT[Item].need].worn] = PLAYER.emptyinv[ITEMS[INTERACT[Item].need].worn]
            INTERACT[Item].quest = True # this turns on the quest flag for the interactable once interacted with if you have the item
            printT(INTERACT[Item].Sinfo + "(\S)") #special slow version
            PLAYER.updateStats()  # TODO stats should automatically update whenver player state is changed
            ITEMS[INTERACT[Item].need].location=(None,None,None) # Brendan added this, used to clear the item location
            if INTERACT[Item].drop:
                MAPS[x][y][z][dim].placeItem(ITEMS[INTERACT[Item].drop])
                print "You see " + ITEMS[INTERACT[Item].drop].name +".\n"
 
            print ""

        elif INTERACT[Item].need == "":  # Has no needed Items (I.E. it's a quest interface)
            INTERACT[Item].quest = True  # this turns on the quest flag so it can trigger quest events
            printT(INTERACT[Item].info)
            printT(INTERACT[Item].Sinfo)
        else:
            printT(INTERACT[Item].info,72,0.1) #fast version
        if GAMESETTINGS['DevMode']:  # If in devmode can see the stats/quest of enemies
            print "NEED : " + str(INTERACT[Item].need)
            print "DROP : " + str(INTERACT[Item].drop)
            print "QUESTFlag : " + str(INTERACT[Item].quest)
    # If you try to inspect a person
    elif Item in ENEMIES and ((list(ENEMIES[Item].location) == PLAYER.location)) and (ENEMIES[Item].alive):
        print "\nIt's rude to stare at people!"

    else:
        print "\nYou can't find that around here. Maybe it's your hungover typing.\n"

def Inventory():
    global PLAYER
    print ""
    # Player inventory is a dictionary of objects so can access and print them out
    print "{1}HEAD: " + PLAYER.inv['head'].name
    print "{2}BODY: " + PLAYER.inv['body'].name
    print "{3}HAND: " + PLAYER.inv['hand'].name
    print "{4}OFF-HAND: " + PLAYER.inv['off-hand'].name
    # This old method is more general/expandable but doesn't do them in order
    # for i in PLAYER.inv:
    #     print i.upper() + ": " + PLAYER.inv[i].name
    print ""
def Eat(Item):
    global PLAYER
    global ITEMS
    global MAPS
    x = PLAYER.location[0]
    y = PLAYER.location[1]
    z = PLAYER.location[2]
    dim = PLAYER.location[3]

    if Item in ITEMS and list(ITEMS[Item].location) == PLAYER.location and not(GAMESETTINGS['HardcoreMode']):
        if Item == "jar of peanut butter" and (PLAYER.name in ["Mitchell Lemieux","Erik Reimers"]):
            print "Oh NO! You're " + PLAYER.name + " ! Don't you remember?\nYOU'RE ALERGIC TO PEANUT BUTTER!\nYou DIE due to your lack of responsibility."
            PLAYER.health = 0
            PLAYER.alive = False
        elif ITEMS[Item].health:
            PLAYER.health = PLAYER.health + ITEMS[Item].health
            PLAYER.health = min(PLAYER.maxhealth, PLAYER.health) #made the minimum of your added health and food so players health doesn't clip over
            PLAYER.health = max(PLAYER.health, 0)  # prevents clipping bellow 0
            print "\nYou've eaten the " + ITEMS[Item].name + "."
            # TODO Reimplement health/food indicators with words
            if GAMESETTINGS['DevMode']: print "\nHEALTH: "+ str(PLAYER.health)+"\n"  # if in DevMode can see stats
            if PLAYER.health == 0:
                PLAYER.alive = False
            ITEMS[Item].location = (None, None, None) #used to clear the item location
            if ITEMS[Item] == PLAYER.inv[ITEMS[Item].worn]:
                PLAYER.inv[ITEMS[Item].worn] = PLAYER.emptyinv[ITEMS[Item].worn]
                ITEMS[Item].location = (None, None, None)
                PLAYER.updateStats()
                print "The " + ITEMS[Item].name + " has been removed from your inventory.\n"
            else:
                MAPS[x][y][z][dim].removeItem(ITEMS[Item])
        else:
            print "You can't eat that!"

    # If you attempt to eat someone
    elif Item in ENEMIES and (list(ENEMIES[Item].location) == PLAYER.location):
        if (ENEMIES[Item].alive):
            printT("You attempt to eat " + Item + "'s arm...(\S) (\S)They pull away ask you to politely Not.")
        else:
            printT("OMG WHAT'S WRONG WITH YOU. I know you're hungry but please find a more vegan option.")

    else:
        print "\nYou can't find that around here. Maybe it's your hungover typing.\n"


# BackEnd Functions
        
def logGame(log): #this makes a log file which records all player actions for debugging
    # TODO add settings and more description to log
    # metacache is a fake name for the log file. As well, saved as .plp for obfuscation purposes
    fpath = GAMEINFO['savepath'] + "MetaChache " + GAMEINFO['playername']+".plp"
    f = open(fpath,"w+")
    for i in range(len(log)):
        f.write(str(log[i]) + '\n')
    f.close()

def NameChange(): # A dumb backend workaround to change the players name. TODO other strategies could have startup instantatied after name is defined
    global PLAYER
    global ENEMIES
    global MAPS
    # ENEMIES['yourself'].name = playername
    ENEMIES['yourself'].name = PLAYER.name # yourself gets renamed to player name
    ENEMIES.update({PLAYER.name.lower():ENEMIES['yourself']}) # adds that new entity to the dictionary
    MAPS[2][4][1][0].placeEnemy(ENEMIES[PLAYER.name.lower()]) # then placed on the map
    # ENEMIES["your dad"].name = playername + "'s dad"
    ENEMIES["your dad"].name = PLAYER.name + "'s dad" # renaming him to your dad
    ENEMIES.update({PLAYER.name.lower():ENEMIES["your dad"]}) # adds that new entity to the dictionary
    MAPS[5][7][1][0].placeEnemy(ENEMIES[PLAYER.name.lower()]) # then placed on the map
    return
        
def SpellCheck(Word,Psblties): #Spellchecks words in the background to check things closest
    Distance = [edit_distance(Word,key) for key in Psblties]
    index = Distance.index(min(Distance))
    return Psblties[index]

def DisplayTime(value): # converts and displays the time given seconds, for speedrunning
    '''From seconds to Days;Hours:Minutes;Seconds'''
    # Figured out there is an effecient way to do this using time module but whatev.
    valueD = (((value/24)/60)/60)
    Days = int (valueD)
    valueH = (value-Days*24*3600)
    Hours = int(valueH/3600)
    valueM = (valueH - Hours*3600)
    Minutes = int(valueM/60)
    valueS = (valueM - Minutes*60)
    Seconds = int(valueS)
    print "Your run-time was: ", Days,"Days; ",Hours,"Hours: ",Minutes,"Minutes; ",Seconds,"Seconds"




###this function definitions were added for the compiler so they don't have to be referenced
def _edit_dist_init(len1, len2):
    lev = []
    for i in range(len1):
        lev.append([0] * len2)  # initialize 2D array to zero
    for i in range(len1):
        lev[i][0] = i           # column 0: 0,1,2,3,4,...
    for j in range(len2):
        lev[0][j] = j           # row 0: 0,1,2,3,4,...
    return lev


def _edit_dist_step(lev, i, j, s1, s2, substitution_cost=1, transpositions=False):
    c1 = s1[i - 1]
    c2 = s2[j - 1]

    # skipping a character in s1
    a = lev[i - 1][j] + 1
    # skipping a character in s2
    b = lev[i][j - 1] + 1
    # substitution
    c = lev[i - 1][j - 1] + (substitution_cost if c1 != c2 else 0)

    # transposition
    d = c + 1  # never picked by default
    if transpositions and i > 1 and j > 1:
        if s1[i - 2] == c2 and s2[j - 2] == c1:
            d = lev[i - 2][j - 2] + 1

    # pick the cheapest
    lev[i][j] = min(a, b, c, d)


def edit_distance(s1, s2, substitution_cost=1, transpositions=False):
    """
    Calculate the Levenshtein edit-distance between two strings.
    The edit distance is the number of characters that need to be
    substituted, inserted, or deleted, to transform s1 into s2.  For
    example, transforming "rain" to "shine" requires three steps,
    consisting of two substitutions and one insertion:
    "rain" -> "sain" -> "shin" -> "shine".  These operations could have
    been done in other orders, but at least three steps are needed.

    Allows specifying the cost of substitution edits (e.g., "a" -> "b"),
    because sometimes it makes sense to assign greater penalties to substitutions.

    This also optionally allows transposition edits (e.g., "ab" -> "ba"),
    though this is disabled by default.

    :param s1, s2: The strings to be analysed
    :param transpositions: Whether to allow transposition edits
    :type s1: str
    :type s2: str
    :type substitution_cost: int
    :type transpositions: bool
    :rtype int
    """
    # set up a 2-D array
    len1 = len(s1)
    len2 = len(s2)
    lev = _edit_dist_init(len1 + 1, len2 + 1)

    # iterate over the array
    for i in range(len1):
        for j in range(len2):
            _edit_dist_step(lev, i + 1, j + 1, s1, s2,
                            substitution_cost=substitution_cost, transpositions=transpositions)
    return lev[len1][len2]
################this is the start of the file

