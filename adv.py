from room import Room
from player import Player
from world import World
from utils import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


#variables and storage

traversal_path = []
walkback = Stack()
visited = {}
opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# methods

# identify exits
def id_exits(current_room):
    exits = current_room.get_exits()

    for exit in exits:
        visited[current_room.id][exit] = current_room.get_room_in_direction(
            exit).id
    return

# check the current room for unused exits
def check_exits(visited, current_room):

    unused_exits = []
    all_exits = current_room.get_exits()

    for exit in all_exits:
        if current_room.get_room_in_direction(exit).id not in visited:
            unused_exits.append(exit)

    if len(unused_exits) > 0:
        return unused_exits

    return None

# randomly select an exit
def choose_exit(visited, current_room):

    valid_exits = check_exits(visited, current_room)

    if valid_exits:
        return random.choice(valid_exits)

        return None

# go through rooms at random until hit a dead end, then go back through each room in order until you find an unused exit. 
def walk_the_maze(visited, current_room):

    rooms = Stack()
    rooms.push(player.current_room)

    while len(visited) < len(world.rooms):
        current_room = rooms.pop()

        if current_room.id not in visited:
            visited[current_room.id] = {}
            if len(visited) == len(world.rooms):
                break

        id_exits(current_room)

        move = choose_exit(visited, current_room)

        if move != None:
            traversal_path.append(move)
            walkback.push(opposites[move])
            player.travel(move)
            rooms.push(player.current_room)
        else:
            backtrack = walkback.pop()
            player.travel(backtrack)
            traversal_path.append(backtrack)
            rooms.push(player.current_room)


walk_the_maze(visited, player.current_room)
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
