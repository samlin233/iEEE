from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

# Create a Colorfight Instance. This will be the object that you interact
# with.
game = Colorfight()

# Connect to the server. This will connect to the public room. If you want to
# join other rooms, you need to change the argument
game.connect(room = 'groupa')
def sortFirst(y):
    return (y.attack_cost/(2*y.energy)+(y.attack_cost/6*y.gold))
def sortSecond(x): 
    return (x.attack_cost/(1*x.energy)+(x.attack_cost/2*x.gold))
# game.register should return True if succeed.
# As no duplicate usernames are allowed, a random integer string is appended
# to the example username. You don't need to do this, change the username
# to your ID.
# You need to set a password. For the example AI, the current time is used
# as the password. You should change it to something that will not change 
# between runs so you can continue the game if disconnected.
if game.register(username = 'ShuaMao', \
        password = "idontknow" ):#, join_key="66466"):
    # This is the game loop
    while True:
        # The command list we will send to the server
        cmd_list = []
        # The list of cells that we want to attack
        my_attack_list = []
        # update_turn() is required to get the latest information from the
        # server. This will halt the program until it receives the updated
        # information. 
        # After update_turn(), game object will be updated.   
        game.update_turn()

        # Check if you exist in the game. If not, wait for the next round.
        # You may not appear immediately after you join. But you should be 
        # in the game after one round.
        if game.me == None:
            continue

        me = game.me
        c_close = set()    
        # game.me.cells is a dict, where the keys are Position and the values
        # are MapCell. Get all my cells.
        for cell in game.me.cells.values():
            # Check the surrounding position

            for pos in cell.position.get_surrounding_cardinals():
                c_close.add(game.game_map[pos])
        for cell in game.me.cells.values():
            if cell.is_home and cell.building.can_upgrade:
                cmd_list.append(game.upgrade(cell.position))
            for pos in cell.position.get_surrounding_cardinals():
                # Get the MapCell object of that position
                if game.turn<=80:
                    sorted(c_close,key = sortSecond)
                    #c_close.sort(key = sortSecond)
                else:
                    sorted(c_close,key = sortFirst)
                    #c_close.sort(key = sortFirst)
                #sorted(c_close, key = lambda x: (x.attack_cost/(2*x.energy))+(x.attack_cost/x.gold))
                for c in c_close:
                # Attack if the cost is less than what I have, and the owner
                # is not mine, and I have not attacked it in this round already
                # We also try to keep our cell number under 100 to avoid tax
                    if game.turn <= 200:
                        lenoft = 600
                    else:
                        lenoft = 900
                    if c.attack_cost < me.energy and c.owner != me.uid \
                            and c.position not in my_attack_list \
                            and len(me.cells) < lenoft:
                    
                    # Add the attack command in the command list
                    # Subtract the attack cost manually so I can keep track
                    # of the energy I have.
                    # Add the position to the attack list so I won't attack
                    # the same cell
                        print("We are attacking ({}, {}) with {} energy".format(pos.x, pos.y, c.attack_cost))
                        game.me.energy -= c.attack_cost
                        my_attack_list.append(c.position)
                        cmd_list.append(game.attack(c.position, c.attack_cost))

            # Build a random building if we have enough gold
            if cell.owner == me.uid and cell.building.is_empty and me.gold >= 100:
                if(game.turn<=80):
                    if cell.gold > cell.energy+2 and cell.gold >= 5:
                        building = (BLD_GOLD_MINE)
                    else:
                        building = (BLD_ENERGY_WELL)

                else:
                    if cell.energy >= cell.gold and cell.energy >= 4:
                        building = (BLD_ENERGY_WELL)
                    elif cell.gold > cell.energy and cell.gold >= 5:
                        building = (BLD_GOLD_MINE)
                    else:
                        building = (BLD_FORTRESS)
                cmd_list.append(game.build(cell.position, building))
                print("We build {} on ({}, {})".format(building, cell.position.x, cell.position.y))
                me.gold -= 100

            # If we can upgrade the building, upgrade it.
            # Notice can_update only checks for upper bound. You need to check
            # tech_level by yourself. 

            if cell.building.can_upgrade and \
                    (cell.building.is_home or cell.building.level < me.tech_level) and \
                    cell.building.upgrade_gold < me.gold and \
                    cell.building.upgrade_energy < me.energy:
                cmd_list.append(game.upgrade(cell.position))
                print("We upgraded ({}, {})".format(cell.position.x, cell.position.y))
                me.gold   -= cell.building.upgrade_gold
                me.energy -= cell.building.upgrade_energy
                


        
        # Send the command list to the server
        result = game.send_cmd(cmd_list)
        print(result)
