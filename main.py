gold = 0
health = 3
deaths = 0

game_state = 0

def print_stats():
    print(f"HP: {health}      Gold: {gold}")

def make_decision(decisions):
    for i, dec in enumerate(decisions):
        num = i + 1
        print(f"{num}. dec")

    print("")
    return int(input("> "))

running = True

while running:
    if game_state == 0:
        print("You wake up in a forest. You don't know how you got there, or what is going on. " \
        "All you know is that you look up to see the sun slowly setting. " \
        "You've heard rummors about people disappearing a night who get lost in the forest. " \
        "You need to get out before you turn into another newspaper story. " \
        "As you look around, you see a path in the distance.")
        choice = make_decision(['Look around the area', 'Follow the path'])

        if choice == 0:
            print("You walk around for a bit, and find a few pieces of gold.")
            gold += 3
            choice = make_decision(['Press Enter to Continue...'])
        elif choice == 1:
            game_state = 1