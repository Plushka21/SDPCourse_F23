from app import App
from bcolors import Bcolors
from user import User
from sport_activity import SportActivty
from datetime import datetime
import json
from typing import Dict, Tuple, Callable

if __name__ == "__main__":
    # Create new empty app
    app = App()

    # In the beginning ask if the user if they want to load stored data into app
    print("Would you like to run demoscenario (Load precreated users and activities)?")
    option_list: Dict[int, str] = {1: "Yes", 2: "No"}
    while True:
        for i, k in option_list.items():
            print(f"{i}: {k}")
        act_num = input("\nEnter preferred option number: ")
        try:
            actual_act_num = int(act_num)
            option_list[actual_act_num]
            break
        except (ValueError, KeyError):
            print(f"{Bcolors.FAIL}You entered wrong number, try again{Bcolors.ENDC}\n")
            continue
    
    # In case of positive answer load data from .JSON file
    if actual_act_num == 1:
        demo_data = json.load(open("data/demo_data.json"))
        
        # Load and create users
        for user in demo_data["Users"]:
            app.add_user(User(user))
        
        # Set one of the users as current one
        app.set_cur_user(app.users["Arthur"])
        
        # Load and create activities for corresponding users
        for act in demo_data["Activities"]:
            author: User= app.users[act["author"]]
            name: str = act["name"]
            dt: datetime = datetime(*[int(n) for n in act["dt"].split(",")])
            place: str = act["place"]
            app.add_activity(SportActivty(author, name, dt, place), author)
    
    # Otherwise ask to create new user right now
    else:
        print(f"\n{Bcolors.OKBLUE}Need to create new user as a current one{Bcolors.ENDC}")
        app.create_user()
        print(f"{Bcolors.OKGREEN}Creted new user. The current user is {Bcolors.OKBLUE}{Bcolors.BOLD}{app.current_user_name}{Bcolors.ENDC}")

    # Actions for main display
    actions: Dict[int, Tuple[str, Callable[[], None]]] = {
        1: ("Create user", app.create_user),
        2: ("Change user", app.change_user),
        3: ("Create activity", app.create_activity),
        4: ("Choose activity", app.choose_activity),
        5: ("Display my activities", app.display_user_activities)
    }
    
    try:
        while True:
            # Always type the name of currently selected user
            print(f"\nThe current user is {Bcolors.OKBLUE}{Bcolors.BOLD}{app.current_user_name}{Bcolors.ENDC}")
            for a in actions:
                print(f"{a:<3}: {actions[a][0]}")

            action_num = input("\nChoose action from the list above: ")
            try:
                actual_act_num = int(action_num)
                action: Callable[[], None] = actions[actual_act_num][1]
            except (ValueError, KeyError):
                print(f"{Bcolors.FAIL}You entered wrong activity number, try again{Bcolors.ENDC}\n")
                continue
            
            # Execute corresponding function
            action()

    except KeyboardInterrupt:
        print(f"\n\n{Bcolors.WARNING}Aborted{Bcolors.ENDC}")
        print(f"{Bcolors.WARNING}App shutdown{Bcolors.ENDC}")