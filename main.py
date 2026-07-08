import hashlib
import hmac
import json
import os

gold = 0
health = 5
deaths = 0
has_sword = False

game_state = 0

SAVE_FILE = 'save.json'

SECRET_KEY = 'tbg-2026-c0nf1d3nt1al-7hr33-by73-k3y-F7c8Z9'

def print_stats():
    print(f"HP: {health}      Gold: {gold}")

def make_decision(decisions):
    print("")
    for i, dec in enumerate(decisions):
        num = i + 1
        print(f"{num}. {dec}")

    print("")
    while True:
        try:
            choice = int(input("> ")) - 1
            if 0 <= choice < len(decisions):
                return decisions[choice]
            print(f"Please enter a number between 1 and {len(decisions)}.")
        except ValueError:
            print("Please enter a valid number.")

def enter_to_continue():
    input("\nPress Enter to Continue...")

def clear_screen():
    os.system("cls")

def set_choices(game_state):
    if game_state == 0:
        choices = ['Look around the area', 'Follow the path']
    elif game_state == 1:
        choices = ['Jump over', 'Walk along side']
    elif game_state == 1.1:
        choices = ['Enter cave', 'Stay out']
    elif game_state == 2:
        choices = ['Search chest on left', 'Search chest on right', 'Continue through cave']
    elif game_state == 3:
        choices = ['Take sword', 'Leave sword']
    elif game_state == 4:
        choices = ['Fight bear (with sword if equipped)', 'Run out of cave']
    else:
        choices = []

    choices.append('Save and quit')
    return choices

possible_choices = set_choices(0)
    
def game_over():
    print("\n GAME OVER")
    input("\nPress Enter to Restart")

    global gold
    global health
    global deaths
    global game_state
    global possible_choices
    global has_sword

    gold = 0
    health = 3
    deaths += 1
    game_state = 0
    possible_choices = set_choices(0)
    has_sword = False

def check_death():
    if health <= 0:
        game_over()
        return True
    return False

def save_game():
    data = {
        'gold': gold,
        'health': health,
        'deaths': deaths,
        'has_sword': has_sword,
        'game_state': game_state,
        'possible_choices': list(possible_choices),
    }
    canonical = json.dumps(data, sort_keys=True)
    signature = hmac.new(SECRET_KEY.encode(), canonical.encode(), hashlib.sha256).hexdigest()
    save_obj = {'data': data, 'signature': signature}
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(save_obj, f, indent=2)
        print(f"\nGame saved to {SAVE_FILE}.")
    except OSError as e:
        print(f"\nCould not save game: {e}")

def load_game():
    global gold, health, deaths, has_sword, game_state, possible_choices

    try:
        with open(SAVE_FILE, 'r') as f:
            save_obj = json.load(f)
        if 'signature' not in save_obj or 'data' not in save_obj:
            print(f"\nSave file is missing integrity signature.")
            return False
        canonical = json.dumps(save_obj['data'], sort_keys=True)
        expected = hmac.new(SECRET_KEY.encode(), canonical.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(save_obj['signature'], expected):
            print(f"\nSave file has been tampered with. Starting fresh.")
            return False
        data = save_obj['data']

        gold = data['gold']
        health = data['health']
        deaths = data['deaths']
        has_sword = data['has_sword']
        game_state = data['game_state']
        saved_choices = data.get('possible_choices')
        if saved_choices is None:
            possible_choices = set_choices(game_state)
        else:
            possible_choices = list(saved_choices)
            if 'Save and quit' not in possible_choices:
                possible_choices.append('Save and quit')
        return True
    except (json.JSONDecodeError, KeyError, OSError) as e:
        print(f"\nCould not load save file: {e}")
        return False

def game_completed():
    clear_screen()
    score = health + gold

    print("\nYou completed the game! Thank you for playing.")
    print("\nScore calculation: Health left over + Gold - Deaths")
    print(f"\nScore: {score}")

running = True

# Startup: offer to load saved game or start new
if os.path.exists(SAVE_FILE):
    try:
        answer = input('Saved game found. Load it? (y/n): ').strip().lower()
    except EOFError:
        print('No input received; starting a new game.')
        answer = 'n'
    if answer.startswith('y'):
        if not load_game():
            print('Starting a new game instead.')
            try:
                os.remove(SAVE_FILE)
            except OSError:
                pass
    elif answer.startswith('n'):
        try:
            os.remove(SAVE_FILE)
        except OSError:
            pass
    else:
        print('Unrecognized input; keeping existing save.')

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

        if choice == 'Save and quit':
            save_game()
            running = False
            continue

        possible_choices.remove(choice)

        if choice == 'Look around the area':
            clear_screen()
            print("You walk around for a bit, and find a few pieces of gold.")
            gold += 3
            enter_to_continue()
            
        elif choice == 'Follow the path':
            possible_choices = set_choices(1)
            game_state = 1

    elif game_state == 1:
        clear_screen()
        print_stats()
        print("After following the path for a little while, you come apon a river. " \
        "If you remember correctly, you've heard that this river is very dangerous because the speed of the water is so fast, that anyone who falls in is sweapt away and rammed into many rocks " \
        "You have two options. " \
        "You can either try your luck and attempt to jump over it, or just walk along the side, hopefully running into the end of it.")

        choice = make_decision(possible_choices)

        if choice == 'Save and quit':
            save_game()
            running = False
            continue

        if choice == 'Jump over':
            clear_screen()
            print("You get a running start, and sprint as fast as you can to the edge of the river. " \
            "You jump as far as you can. " \
            "It looks like you're gonna make it! " \
            "But you just barely miss the ledge and fall into the river.")

            game_over()

        elif choice == 'Walk along side':
            possible_choices = set_choices(1.1)
            clear_screen()
            print("You decide to play it safe and walk by the side of the river, but you hope to escape the forrest before nightfall. " \
            "As you continue to walk along side the river, you notice the sun setting over the horizon. " \
            "It's almost night time!" \
            "After a while of walking, you run into a cave where the water is running into. " \
            "You can either keep walking and risk staying out at night, or enter the cave for safety.")

            choice = make_decision(possible_choices)

            if choice == 'Save and quit':
                save_game()
                running = False
                continue

            if choice == 'Enter cave':
                possible_choices = set_choices(2)
                game_state = 2
            elif choice == 'Stay out':
                clear_screen()
                print("You decide to stay out during the night, but after the sun sets you feel something watching you from behind. " \
                "You turn around to see a pack of wolves stalking you from a distance. " \
                "After you hold eye contact with them for a little bit, not moving a muscle, they dart towards you, and you start running as fast as you can. " \
                "You see the cave in the distance, and determine it's your only chance of survival. As you make you're way to the cave, you trip and fall, and one of the wolves catches up to you. " \
                "But you quickly get up and make it into the cave with only a slight claw mark from the wolf, and they all left you alone. " \
                "\n\n-2 HP")

                health -= 2

                if check_death():
                    continue

                enter_to_continue()

                possible_choices = set_choices(2)
                game_state = 2
    
    elif game_state == 2:
        clear_screen()
        print_stats()
        print("As you slowly walk into the cave, you see that the cave is lit up with light, even though it should be a very dark cave. " \
        "After some searching, you realize the water appears to be giving off some sort of light. " \
        "After walking a little further, you see 2 chests sitting on the sides of the cave. " \
        "How did they get there? " \
        "What do you want to do?")

        choice = make_decision(possible_choices)

        if choice == 'Save and quit':
            save_game()
            running = False
            continue

        possible_choices.remove(choice)

        if choice == 'Search chest on left':
            clear_screen()
            print("As you slowly open the chest, you see what appears to be gold sitting in the chest. Nice! " \
            "\n\n+1 Gold")

            gold += 1

            enter_to_continue()
        elif choice == 'Search chest on right':
            clear_screen()
            print("As you slowly open the chest, you are quickly attacked by a little spider, but it doesn't do much, since it's very small. " \
            "\n\n-1 HP")

            health -= 1

            if check_death():
                continue

            enter_to_continue()
        elif choice == 'Continue through cave':
            possible_choices = set_choices(3)
            game_state = 3

    elif game_state == 3:
        clear_screen()
        print_stats()
        print("As you continue through the cave, you start to notice something shining in the back. " \
        "You walk up to investigate when you realize it's a sword! This may be useful later.")

        choice = make_decision(possible_choices)

        if choice == 'Save and quit':
            save_game()
            running = False
            continue

        possible_choices.remove(choice)

        if choice == 'Take sword':
            clear_screen()
            print("You slowly pick the sword up out of the ground, and you suddenly gain a bit of hopefulness")

            has_sword = True

            enter_to_continue()

            possible_choices = set_choices(4)
            game_state = 4
        elif choice == 'Leave sword':
            clear_screen()
            print("Not wise, you don't know what's could be in the cave...")

            enter_to_continue()

            possible_choices = set_choices(4)
            game_state = 4

    elif game_state == 4:
        clear_screen()
        print_stats()
        print("As you continue to walk through the cave, you notice a strange sound coming from infront of you, but it's too dark to see right now. " \
        "(Where's that glowing water when you need it?) " \
        "As you slowly creep forward, you begin to see a giant silhouette. " \
        "You finally realize it's a bear!")

        choice = make_decision(possible_choices)

        if choice == 'Save and quit':
            save_game()
            running = False
            continue

        possible_choices.remove(choice)

        if choice == 'Fight bear (with sword if equipped)':
            if has_sword:
                clear_screen()
                print("You raise your sword to fight the bear, but he gracefully swipes it out of your grasp. " \
                "In terror you quickly run out of the cave, and as far away as you can get.")

                enter_to_continue()

                possible_choices = set_choices(5)
                game_state = 5
            else:
                clear_screen()
                print("As you try to fight the bear with your bare hands, (get it :)) he easily gets a good hit on you, and your vision slowly fades...\n\n-4 HP")
                
                health -= 4

                if check_death():
                    continue
                
                print("But you get back up! With the last bit of strength remaining inside of you, you run for the exit of the cave as fast of you can, not turning back for one second.")

                possible_choices = set_choices(5)
                game_state = 5
        elif choice == 'Run out of cave':
            clear_screen()
            print("You turn for the exit and run as fast as you can, not turning back for a second. (good idea)")

            enter_to_continue()

            possible_choices = set_choices(5)
            game_state = 5

    elif game_state == 5:
        clear_screen()
        print_stats()
        print("After getting as far away from the cave as you possibly can, you finally slow down from your running and walk at a slow pace to catch your breath. " \
        "After walking for a while, you find yourself at a village. " \
        "You finally made your way out of the forrest! " \
        "You're safe!")

        enter_to_continue()

        game_completed()

        running = False