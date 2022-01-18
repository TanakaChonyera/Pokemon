########################################################################################################################
#
#       CS Programming Project #11
#
#           Algorithm
#
#               Start
#
#                   Import modules
#                   function definitions
#                   Prompt user for input
#                       Loop until user quits
#                           Get pokemon list
#                           Get pokemon moves list
#                           Prompt player 1 for pokemon selection
#                               Loop while input incorrect
#                           Initialise Player 1
#                           Prompt player 2 for pokemon selection
#                               Loop while input incorrect
#                           Initialise Player 2
#                           Call relevant functions (which manage the game)
#
#               End
#
########################################################################################################################
import csv
from random import randint
from random import seed
from copy import deepcopy

from pokemon import Pokemon
from pokemon import Move

seed(1)  # Set the seed so that the same events always happen

# DO NOT CHANGE THIS!!!
# =============================================================================
element_id_list = [None, "normal", "fighting", "flying", "poison", "ground", "rock",
                   "bug", "ghost", "steel", "fire", "water", "grass", "electric",
                   "psychic", "ice", "dragon", "dark", "fairy"]


# Element list to work specifically with the moves.csv file.
#   The element column from the moves.csv files gives the elements as integers.
#   This list returns the actual element when given an index
# =============================================================================

def read_file_moves(fp):
    '''
        This function takes in the file pointer created from opening the moves.csv file and
            returns a list of move objects.
    '''

    list_of_moves = []

    with fp as file:

        reader = csv.reader(file)

        # Skip header line
        next(reader, None)

        for line in reader:

            if line[9] == '1' or line[2] != '1' or line[4] == '' or line[6] == '':
                continue
            else:
                move_object = Move(line[1], element_id_list[int(line[3])], int(line[4]), int(line[6]), int(line[9]))
                list_of_moves.append(move_object)

    return list_of_moves


def read_file_pokemon(fp):
    '''
        This function takes in the file pointer created from opening the pokemon.csv file and
        returns a list of pokemon objects.
    '''

    list_of_pokemon = []
    id_list = []

    with fp as file:

        reader = csv.reader(file)

        # Skip header line
        next(reader, None)

        for line in reader:

            if line[11] != '1' or line[0] in id_list:
                continue
            else:
                pokemon_object = Pokemon(line[1].lower(), line[2].lower(), line[3].lower(), None, int(line[5]), \
                                         int(line[6]), int(line[7]), int(line[8]), int(line[9]))

                list_of_pokemon.append(pokemon_object)
                id_list.append(line[0])

        return list_of_pokemon


def choose_pokemon(choice, pokemon_list):
    '''
        This function takes in user input (called choice) as a string and the list of available
        pokemon. If the user input is an integer, the integer becomes the index for selecting a
        pokemon from the pokemon_list and a deepcopy of the pokemon object at that index is
        returned.
    '''

    choice_str = False
    i_choose_you = None

    # choice = input("Player {}, choose a pokemon by name or index: ".format('something'))

    # Check data type of user
    try:
        int(choice)
    except ValueError:
        choice_str = True
        choice = choice.lower()

    # Get pokemon object and make deepcopy so as not to change the original
    if choice_str:
        for index, pokemon_object in enumerate(pokemon_list):
            if choice == pokemon_object.name:
                i_choose_you = deepcopy(pokemon_object)
    else:
        for index, pokemon_object in enumerate(pokemon_list):
            if int(choice) - 1 == index:
                i_choose_you = deepcopy(pokemon_object)

    return i_choose_you


def add_moves(pokemon, moves_list):
    '''
        This function first adds one random move to the pokemon’s move list, then adds three
        more moves that match one of the elements of this pokemon.
    '''

    attempts = 0

    random_int = randint(0, len(moves_list) - 1)
    random_move = moves_list[random_int]

    pokemon.add_move(random_move)

    while len(pokemon.moves) != 4 and attempts <= 200:

        attempts += 1

        random_int = randint(0, len(moves_list) - 1)
        random_move = moves_list[random_int]

        if (random_move.get_element() == pokemon.element1 or random_move.get_element() == pokemon.element2) and \
                random_move not in pokemon.moves:

            pokemon.add_move(random_move)

        else:
            continue

    if len(pokemon.moves) == 4:
        return True
    else:
        return False


def turn(player_num, player_pokemon, opponent_pokemon):
    '''
        Manages outputs for players.
    '''

    print("Player {}'s turn".format(player_num))
    print(player_pokemon)

    while True:

        usr_int_str = False

        print("Show options: \'show ele\', \'show pow\', \'show acc\'")
        usr_inp = input("Select an attack between 1 and {} or show option or 'q': ".format(len(player_pokemon.moves)))

        try:
            int(usr_inp)
        except ValueError:
            usr_int_str = True

        if usr_int_str:

            if usr_inp.lower() == 'show ele':
                print('{:<15}{:<15}{:<15}{:<15}'.format(player_pokemon.moves[0].get_element(), \
                                                        player_pokemon.moves[1].get_element(), \
                                                        player_pokemon.moves[2].get_element(), \
                                                        player_pokemon.moves[3].get_element()))

            elif usr_inp.lower() == 'show pow':
                print('{:<15}{:<15}{:<15}{:<15}'.format(player_pokemon.moves[0].get_power(), \
                                                        player_pokemon.moves[1].get_power(), \
                                                        player_pokemon.moves[2].get_power(), \
                                                        player_pokemon.moves[3].get_power()))

            elif usr_inp.lower() == 'show acc':
                print('{:<15}{:<15}{:<15}{:<15}'.format(player_pokemon.moves[0].get_accuracy(), \
                                                        player_pokemon.moves[1].get_accuracy(), \
                                                        player_pokemon.moves[2].get_accuracy(), \
                                                        player_pokemon.moves[3].get_accuracy()))

            elif usr_inp.lower() == 'q':

                if player_num - 1 == 0:
                    player_won = 2
                else:
                    player_num = 1

                print("Player {} quits, Player {} has won the pokemon battle!".format(player_num, \
                                                                                      player_won))
                return False

        else:

            print('selected move:', player_pokemon.moves[int(usr_inp) - 1])
            print()
            display = opponent_pokemon.name + ' hp before:' + str(opponent_pokemon.hp)
            print(display)
            player_pokemon.attack(player_pokemon.moves[int(usr_inp) - 1], opponent_pokemon)
            display = opponent_pokemon.name + ' hp after:' + str(opponent_pokemon.hp)
            print(display)
            print()

            if opponent_pokemon.hp == 0:

                if int(player_num) == 1:
                    player_lost = 1
                    player_won = 2
                else:
                    player_lost = 2
                    player_won = 1

                print("Player {}'s pokemon fainted, Player {} has won the pokemon battle!".format(player_won, \
                                                                                                  player_lost))
                return False

            break

    return True


def main():

    valid_pokemon = True

    usr_inp = input("Would you like to have a pokemon battle? ").lower()
    while usr_inp != 'n' and usr_inp != 'q' and usr_inp != 'y':
        usr_inp = input("Invalid option! Please enter a valid choice: Y/y, N/n or Q/q: ").lower()

    if usr_inp != 'y':
        print("Well that's a shame, goodbye")
        return

    while True:

        if usr_inp == 'y':

            pokemon_list = read_file_pokemon(open('pokemon.csv', 'r'))
            pokemon_moves = read_file_moves(open('moves.csv', 'r'))

            player1_choice = input("Player {}, choose a pokemon by name or index: ".format(1))
            player1_pokemon = choose_pokemon(player1_choice, pokemon_list)

            if player1_pokemon is None:
                valid_pokemon = False
            else:
                try:
                    bool(player1_pokemon)
                    valid_pokemon = True
                except:
                    valid_pokemon = False

            while True:

                if valid_pokemon is False:
                    "Invalid option, choose a pokemon by name or index: "
                    player1_choice = input("Invalid option, choose a pokemon by name or index: ")
                    player1_pokemon = choose_pokemon(player1_choice, pokemon_list)

                    if player1_pokemon is None:
                        valid_pokemon = False
                    else:
                        try:
                            bool(player1_pokemon)
                            valid_pokemon = True
                        except:
                            valid_pokemon = False

                else:

                    break

            add_moves(player1_pokemon, pokemon_moves)
            print('pokemon1:')
            print(player1_pokemon.__repr__())

########################################################################################################################

            valid_pokemon = True

            player2_choice = input("Player {}, choose a pokemon by name or index: ".format(2))
            player2_pokemon = choose_pokemon(player2_choice, pokemon_list)

            # Validation check for pokemon
            if player2_pokemon is None:
                valid_pokemon = False
            else:
                try:
                    bool(player2_pokemon)
                    valid_pokemon = True
                except:
                    valid_pokemon = False

            while True:

                if valid_pokemon is False:
                    "Invalid option, choose a pokemon by name or index: "
                    player2_choice = input("Invalid option, choose a pokemon by name or index: ")
                    player2_pokemon = choose_pokemon(player2_choice, pokemon_list)

                    # Validation check for pokemon
                    if player2_pokemon is None:
                        valid_pokemon = False
                    else:
                        try:
                            bool(player2_pokemon)
                            valid_pokemon = True
                        except:
                            valid_pokemon = False

                else:

                    break

            add_moves(player2_pokemon, pokemon_moves)
            print('pokemon2:')
            print(player2_pokemon.__repr__())

            while True:

                next_round = turn(1, player1_pokemon, player2_pokemon)
                if next_round is False:
                    break

                if next_round:
                    next_round = turn(2, player2_pokemon, player1_pokemon)
                    if next_round is False:
                        break

                    if next_round:
                        print('Player 1 hp after:', player1_pokemon.get_hp())
                        print('Player 2 hp after:', player2_pokemon.get_hp())
                        continue
                    else:
                        break

            go_again = input("Battle over, would you like to have another? ")

            if go_again.lower() == 'y':
                pass
            elif go_again.lower() == 'n' or go_again.lower() == 'q':
                print("Well that's a shame, goodbye")
                break
            else:
                while True:
                    go_again = input("Invalid option! Please enter a valid choice: ")
                    if go_again.lower() == 'y':
                        break
                    elif go_again.lower() == 'n' or go_again.lower() == 'q':
                        print("Well that's a shame, goodbye")
                        return
                    else:
                        continue

    else:
        pass

if __name__ == "__main__":
    main()
