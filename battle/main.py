from classes.game import Person, bcolors
from classes.magic import spell
from classes.inventory import Item
import random
from time import sleep
from random import uniform
import sys
lines = [bcolors.FAIL + bcolors.BOLD + "The Enemies attacked §╦§" + bcolors.ENDC,
         bcolors.OKGREEN + "YOU are champions. GO FIGHT!!!" + bcolors.ENDC,
         "HP : HIT POINTS   MP : MAGIC POINTS",
         "GO SAVE YOURSELF"]

for line in lines:
    for c in line:
        print(c, end='')
        sys.stdout.flush()
        sleep(uniform(0.05, 0.06))
    print('')

# Creating Black Magic

Fire = spell("Fire", 25, 600, "black")
Thunder = spell("Thunder", 27, 610, "black")
Blizzard = spell("Blizzard", 26, 600, "black")
Meteor = spell("Meteor", 40, 1200, "black")
Quake = spell("Quake", 34, 740, "black")

# Creating White Magic

Cure = spell("Cure", 25, 400, "White")
Hpotion = spell("Magical  Potion", 32, 500, "White")
curaga = spell("Curaga", 50, 3000, "White")


#Create some Items

potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("HI-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Partially restores HP/MP of some party member", 2000)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Assigning lists
player_spells = [Fire, Thunder, Blizzard, Meteor, Quake, Cure, Hpotion]
enemy_spells = [Fire, Meteor, curaga]

player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 7},
                {"item": elixer, "quantity": 8},
                {"item": hielixer, "quantity": 5},
                {"item": grenade, "quantity": 5}]

# Instantiate People

player1 = Person("Joey    : ", 3880, 132, 300, 34, player_spells, player_items)
player2 = Person("Ross    : ", 3964, 188, 310, 34, player_spells, player_items)
player3 = Person("Chandler: ", 4120, 174, 288, 34, player_spells, player_items)


enemy1 = Person("Goblin     ", 1300, 130, 400, 325, enemy_spells, [])
enemy2 = Person("Pinku      ", 9999, 750, 535, 25, enemy_spells, [])
enemy3 = Person("Wizard     ", 1300, 200, 325, 300, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

while running:
    print("===========================================\nPlayers :\n")
    bb = (bcolors.BOLD + bcolors.UNDERLINE + bcolors.WARNING + "NAME" + bcolors.ENDC
          + "                               " + bcolors.UNDERLINE + bcolors.WARNING + "HP" + bcolors.ENDC +
          "                              " + bcolors.UNDERLINE + bcolors.WARNING + "MP" + bcolors.ENDC + bcolors.ENDC)
    for c in bb:
        print(c, end='')
        sys.stdout.flush()
        sleep(0.005)
    print('')

    for player in players:
        player.get_stats()
    print("\n")

    print(bcolors.BOLD + bcolors.WARNING + "ENEMIES: " + bcolors.ENDC)
    for enemy in enemies:
        enemy.enemy_get_stats()

    for player in players:
        player.choose_action()
        while True:
            choice = int(input("\n    choose action: "))
            if (choice <= 0) or (choice > 3):
                print(bcolors.FAIL + "Choose the Correct Action" + bcolors.ENDC)
                continue
            else:
                break

        index = choice - 1
        print("\nYou chose:", str(player.lolipop(index)))

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace("  ", "") + " for", dmg, " points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace("  ", "") + "has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            print(bcolors.UNDERLINE + "\nPress 0 if You want to go to the previous menu" + bcolors.ENDC)
            while True:
                ext = int(input("    Choose magic: "))
                if (ext < 0) or(ext > 7):
                    print(bcolors.FAIL + "Input the correct magic choice\n" + bcolors.ENDC)
                    continue
                else:
                    break

            magic_choice = ext - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n" + "Not enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "White":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " +
                      enemies[enemy].name.replace("  ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace("  ", "") + "has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            print(bcolors.UNDERLINE + "\nPress 0 if You want to go to the previous menu" + bcolors.ENDC)

            while True:
                xet = int(input("Choose Item: "))
                if (xet < 0) or (xet > 6):
                    print(bcolors.FAIL + "Enter the correct Item choice" + bcolors.ENDC)
                    continue
                else:
                    break
            item_choice = xet - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "None Left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " points of Damage." +
                      bcolors.ENDC)

            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restored HP/MP." + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to " +
                      enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace("  ", "") + " has died.")
                    del enemies[enemy]
    print("\n")


# check if battle is over
    defeated_enemies = 0
    defeated_players = 0
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1


# check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win!!!" + bcolors.ENDC)
        break
# Check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your Enemy have beaten You!!!" + bcolors.ENDC)
        break


# enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(bcolors.OKBLUE + enemy.name.replace("  ", ""), " attacks " + players[target].name.replace("  ", "") +
                  " for ", enemy_dmg, "points of damage." + bcolors.ENDC)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == "White":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name.replace("  ", "") +
                      " for", str(magic_dmg), "HP." + bcolors.ENDC)

            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + enemy.name.replace("  ", "") + "'s " + spell.name +
                      " deals", str(magic_dmg), "points of damage to " + players[target].name.replace("  ", "") +
                      bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace("  ", "") + "has died.")
                    del players[target]







