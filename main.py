import os

gold = 0
health = 3
deaths = 0

game_state = 0

def print_stats():
    print(f"HP: {health}      Gold: {gold}")

def make_decision(decisions):
    print("")
    for i, dec in enumerate(decisions):
        num = i + 1
        print(f"{num}. {dec}")

    print("")
    choice = int(input("> ")) - 1

    return decisions[choice]

def enter_to_continue():
    input("\nPress Enter to Continue...")

def clear_screen():
    os.system("cls")

def set_choices(game_state):
    if game_state == 0:
        return ['Look around the area', 'Follow the path']
    elif game_state == 1:
        return ['Jump over', 'Walk along side']

possible_choices = set_choices(0)

running = True

while running:
    if game_state == 0:
        clear_screen()
        print_stats()
        print("You wake up in a forest. You don't know how you got there, or what is going on. " \
        "All you know is that you look up to see the sun slowly setting. " \
        "You've heard rummors about people disappearing a night who get lost in the forest. " \
        "You need to get out before you turn into another newspaper story. " \
        "As you look around, you see a path in the distance.")

        choice = make_decision(possible_choices)

        possible_choices.remove(choice)

        if choice == 'Look around the area':
            clear_screen()
            print("You walk around for a bit, and find a few pieces of gold.")
            gold += 3
            enter_to_continue()
            
        elif choice == 'Follow the path':
            possible_choices = set_choices(1)
            game_state = 1

        print(f"Choice is {choice}")