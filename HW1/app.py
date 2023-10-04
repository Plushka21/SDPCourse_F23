from sport_activity import SportActivty
from user import User
from bcolors import Bcolors
from datetime import datetime
from typing import Dict, List, Optional

class App:
    """class App. This class allows to initialise an app that contains information about axisiting users and their created activities"""
    def __init__(self) -> None:
        self.__user_list: Dict[str, User] = {} # all users in the app
        self.__cur_user: Optional[User] = None # currently selected user
        self.__possible_activities: List = [] # possible activities that users can create
        # fill list of possible activities
        for line in open("data/activities_list.txt", "r").readlines():
            self.__possible_activities.append(line[:-1])
        self.__user_activities: Dict[User, List[SportActivty]] = {}

    @property
    def is_first_user(self) -> bool:
        return self.__cur_user is None

    @property
    def users(self) -> Dict[str, User]:
        return self.__user_list
    
    @property
    def current_user_name(self) -> str:
        return self.__cur_user.name
        
    def set_cur_user(self, user: User) -> None:
        self.__cur_user = user

    def add_user(self, new_user: User) -> None:
        self.__user_list[new_user.name] = new_user
    
    def create_user(self) -> None:
        """Function to create new user"""
        
        print("\nCreating new user now")
        is_name_valid = False
        while not is_name_valid:
            user_name = input("Enter user's name: ")
            # Check if there is already user with the same name
            if user_name in self.users:
                # If so, ask user what to do: either enter new unique user name, or rewrite existing user
                print(f"\n{Bcolors.WARNING}There is already user with the same name what would you like to do?{Bcolors.ENDC}")
                option_list: Dict[int, str] = {1: "Enter new user name", 2: "Rewrite existing user"}
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
                
                # If user decided to rewrite the exisiting user, we need to remove all activities cerated by that user
                if actual_act_num == 2:
                    is_name_valid = True
                    old_user = self.users[user_name]
                    if old_user in self.__user_activities:
                        self.__user_activities.pop(old_user)
            else:
                is_name_valid = True
            
        # Create new user with given name
        new_user = User(user_name)
        self.add_user(new_user)
        print(f"{Bcolors.OKGREEN}Saved new user{Bcolors.ENDC}\n")

        # If there are no users in app, set the new user as the current one
        if self.is_first_user:
            self.set_cur_user(new_user)
        
        # Otherwise give an option to select just created user as current one
        else:
            print("Would you like select created user as the current one?")
            option_list = {1: "Yes", 2: "No"}
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
            
            if actual_act_num == 1:
                self.set_cur_user(new_user)
    
    def change_user(self) -> None:
        """Function to switch current user"""
        
        print(f"Select user from existing:\n")
        for n in self.users:
            print(n)
        
        # Ask to enter the preferred user name
        user_name = input("\nEnter desired user name: ")
        while user_name not in self.users.keys():
            print(f"{Bcolors.FAIL}[ERROR]: Entered non-exisiting name. Try again{Bcolors.ENDC}")
            user_name = input("Enter desired user name: ")
        
        # Update currently selected user
        self.set_cur_user(self.__user_list[user_name])
        print(f"{Bcolors.OKGREEN}Successfully chose new user. The current user is {Bcolors.OKBLUE}{Bcolors.BOLD} {user_name} {Bcolors.ENDC}")
    
    def add_activity(self, new_activity:SportActivty, user_author:User) -> None:
        """Function to add created activity to the existing activities for given user"""
        
        user_act_list = self.__user_activities.get(user_author, [])
        user_act_list.append(new_activity)
        # Sort activities by date for given user
        self.__user_activities[user_author] = sorted(user_act_list, key=lambda activity: activity.planned_at)
    
    def create_activity(self) -> None:
        """Function to create new activty"""

        print(f"\nCreating activity for user {Bcolors.OKBLUE}{Bcolors.BOLD}{self.current_user_name}{Bcolors.ENDC}")
        
        # Ask to enter activity number from suggested list until valid number is entered
        is_num_correct = False
        while not is_num_correct:
            print("\nSelect activity number from the list:")
            for i, a in enumerate(self.__possible_activities):
                print(f"{i+1}: {a}")
            act_num = input("\nEnter preferred activity number: ")

            try:
                actual_act_num = int(act_num)
                is_num_correct = 1 <= actual_act_num <= len(self.__possible_activities)
            except (ValueError, KeyError):
                print(f"{Bcolors.FAIL}You entered wrong number, try again{Bcolors.ENDC}\n")
                continue

        act_name = self.__possible_activities[actual_act_num - 1]

        # Ask to enter date and time of planned activity until valid datetime entered
        is_date_correct = False
        print("\nNow enter activity date and time")
        while not is_date_correct:
            year = int(input('Enter a year: '))
            month = int(input("Enter a month: "))
            day = int(input("Enter a day: "))

            hours = int(input("Enter the hour: "))
            minutes = int(input("Enter the minutes: "))
            
            try:
                datetime(year, month, day, hours, minutes, 0)
                is_date_correct = True
            except ValueError:
                print(f"{Bcolors.FAIL}You entered wrong data format, try again{Bcolors.ENDC}\n")

        dt = datetime(year, month, day, hours, minutes, 0)

        # Ask to enter location of activty
        place = input("\nEnter location: ")

        # Save activty
        new_act = SportActivty(self.__cur_user, act_name, dt, place)
        self.add_activity(new_act, self.__cur_user)
        print(f"Created activity {act_name} at {place} on {dt}")

    def choose_activity(self) -> None:
        """Function to select activty from all activities created by all users"""

        # If there are no activites yet, print the message and leave function
        if len(self.__user_activities) == 0:
            print(f"\n{Bcolors.WARNING}Unfortunately, there is no available activity for you.\nExiting now.{Bcolors.ENDC}")
            return
        
        is_num_correct = False
        current_activities: List[SportActivty] = []
        for act in self.__user_activities.values():
            current_activities.extend(act)

        # Otherwise ask to enter number of suggested activities until valid number is entered
        while not is_num_correct:
            print("\nYou can choose liked activity from the list below.\nOr type 'n' if you want to cancel this option\n")

            for i, act in enumerate(current_activities):
                print(f"{i+1}: {act.name}, {act.planned_at}, {act.place}")

            act_num = input("\nEnter activity number: ")
            if act_num[0].lower() == "n":
                print("\nYou exited activity selection")
                return
            
            try:
                actual_act_num = int(act_num)
            except ValueError:
                print(f"{Bcolors.FAIL}You entered wrong activity number, try again{Bcolors.ENDC}\n")
                continue

            is_num_correct = 1 <= actual_act_num <= len(current_activities)
        
        # Print message about selected activty
        selected_act = current_activities[actual_act_num-1]
        print(f"\n{Bcolors.OKGREEN}Nice choice!{Bcolors.ENDC} Please come to {Bcolors.OKCYAN}{selected_act.place}{Bcolors.ENDC} on {Bcolors.OKCYAN}{selected_act.planned_at}{Bcolors.ENDC}, to play {Bcolors.OKGREEN}{selected_act.name}{Bcolors.ENDC} with {Bcolors.OKBLUE}{selected_act.author.name}{Bcolors.ENDC} there.")
    
    def display_user_activities(self) -> None:
        """Function to display all activites created by the current user"""
        user_act_list = self.__user_activities[self.__cur_user]
        if len(user_act_list) == 0:
            print(f"\n{Bcolors.WARNING}You haven't created any activity yet.. :({Bcolors.ENDC}\n")
            return
        
        print("\nYou've created the following activites by now:\n")
        for a in user_act_list:
            print(f"{a.name} {a.planned_at}, {a.place}")
        
        print()
