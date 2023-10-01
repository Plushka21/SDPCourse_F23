from SportActivity import SportActivty
from User import User
from Bcolors import Bcolors
from datetime import datetime

class App:
    def __init__(self): #, user_list_path="data/user_list.json", act_list_path="data/act_list.json") -> None:
        # self.__user_path = user_list_path
        # self.__act_path = act_list_path
        # self.__user_list = json.load(open(self.__user_path))
        # self.__act_list = json.load(open(self.__act_path))
        self.__user_list = {}
        self.__act_list = {}
        self.__possible_activities = {"1": "Basketball", "2": "Volleyball", "3": "Tennis", "4": "Football"}
        self.__counter = 1

        self.get_user_list = lambda: self.__user_list
        self.get_act_list = lambda: self.__act_list
        self.get_activities = lambda: self.__possible_activities
        self.get_cur_user = lambda cond: self.__cur_user.get_name() if cond else self.__cur_user
        self.__first_user = True
    
    def set_cur_user(self, user: User):
        self.__cur_user = user

    ## TODO: add decorator to check if name is string
    def create_user(self):
        print("\nCreating new user now")
        is_name_valid = False
        while not is_name_valid:
            user_name = input("Enter user's name: ")
            if user_name in self.get_user_list():
                print("\n1: Enter new name\n2: Rewrite user\n")
                action_num = input(f"{Bcolors.WARNING}There is already user with the same name what would you like to do?{Bcolors.ENDC}\nChoose action from the list above ")

                if action_num == "2":
                    is_name_valid = True
            else:
                is_name_valid = True
            

        new_user = User(user_name)
        self.__user_list[user_name] = new_user
        print(f"{Bcolors.OKGREEN}Saved new user{Bcolors.ENDC}\n")


        if self.__first_user:
            self.set_cur_user(new_user)
            self.__first_user = False
        else:
            print("Would you like select created user as the current one?")
            option_list = {"1": "Yes", "2": "No"}
            is_num_correct = False
            while not is_num_correct:
                for i, k in option_list.items():
                    print(f"{i}: {k}")
                act_num = input("\nEnter preferred option number: ")
                if act_num in option_list:
                    is_num_correct = True
                else:
                    print(f"{Bcolors.FAIL}You entered wrong number, try again{Bcolors.ENDC}\n")
            if act_num == "1":
                self.set_cur_user(new_user)

        
        # with open(self.__user_path,'r+') as file:
        #     file_data = json.load(file)
        #     file_data[user_name] = user_name
        #     file.seek(0)
        #     json.dump(file_data, file)#, indent = 4)
    
    def change_user(self):
        print(f"Select user from existing:")
        for n in self.get_user_list():
            print(n)
        
        user_name = input("Enter desired user name: ")
        while user_name not in self.get_user_list().keys():
            print(f"{Bcolors.FAIL}[ERROR]: Entered non-exisiting name. Try again{Bcolors.ENDC}")
            user_name = input("Enter desired user name: ")
        
        self.set_cur_user(self.__user_list[user_name])
        print(f"{Bcolors.OKGREEN}Successfully chose new user. The current user is {Bcolors.OKBLUE}{Bcolors.BOLD} {user_name} {Bcolors.ENDC}")
    
    def create_activity(self): #, user:User, name, time, place):
        print(f"\nCreating activity for user {Bcolors.OKBLUE}{Bcolors.BOLD}{self.get_cur_user(True)}{Bcolors.ENDC}")
        
        poss_activities = self.get_activities()
        is_num_correct = False
        while not is_num_correct:
            print("\nSelect activity number from the list:")
            for i, a in poss_activities.items():
                print(f"{i}: {a}")
            act_num = input("\nEnter preferred activity number: ")
            # poss_activities[act_num]
            if act_num in poss_activities:
                is_num_correct = True
            else:
                print(f"{Bcolors.FAIL}You entered wrong activity number, try again{Bcolors.ENDC}\n")

        # act_name = input("\nEnter activity's name: ")
        act_name = poss_activities[act_num]

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
        place = input("\nEnter location: ")

        new_act = SportActivty(self.__cur_user, act_name, dt, place)
        self.__act_list[str(self.__counter)] = new_act
        self.__counter += 1

        self.__cur_user.get_act_list().append(new_act)
        print(f"Created activity {act_name} at {place} on {dt}")
    
    def check_available_activities(fun):
        def inner_fun(arg):
            if len(arg.__act_list) == 0:
                print(f"\n{Bcolors.WARNING}Unfortunately, there is no available activity for you.\nExiting now.{Bcolors.ENDC}")
                return
            fun(arg)
        return inner_fun

    @check_available_activities
    def choose_activity(self):
        is_num_correct = False
        while not is_num_correct:
            print("\nYou can choose liked activity from the list below.\nOr type 'n' if you want to cancel this option\n")

            for i, a in self.__act_list.items():
                if a.get_author() != self.__cur_user:
                    print(f"{i}: {a.get_name()}, {a.get_time()}, {a.get_place()}")

            act_num = input("\nEnter activity number: ")
            if act_num[0].lower() == "n":
                print("\nYou exited activity selection")
                return

            elif act_num in self.__act_list:
                is_num_correct = True
            else:
                print(f"{Bcolors.FAIL}You entered wrong activity number, try again{Bcolors.ENDC}\n")
        
        selected_act = self.__act_list[act_num]
        print(f"\n{Bcolors.HEADER}Nice choice!{Bcolors.ENDC} Please come to {selected_act.get_place()} on {selected_act.get_time()}, you'll meet {Bcolors.OKBLUE}{selected_act.get_author().get_name()}{Bcolors.ENDC} there.")
    
    def display_user_activities(self):
        user_act_list = self.__cur_user.get_act_list()
        if len(user_act_list) == 0:
            print(f"\n{Bcolors.WARNING}You haven't created any activity yet.. :({Bcolors.ENDC}\n")
            return
        
        print("\nYou've created the following activites by now:\n")
        for a in user_act_list:
            print(f"{a.get_name():<15} {a.get_time()}, {a.get_place()}")
        
        print()


# TODO: add demo scenario with already cerated users and activities
try:
    app = App()
    print(f"\n{Bcolors.OKBLUE}Need to create new user as a current one{Bcolors.ENDC}")
    app.create_user()
    print(f"{Bcolors.OKGREEN}Creted new user. The current user is {Bcolors.OKBLUE}{Bcolors.BOLD}{app.get_cur_user(True)}{Bcolors.ENDC}")

    action_list = {"1": ["Create user", "app.create_user()"], "2": ["Change user", "app.change_user()"], \
                   "3": ["Create activity", "app.create_activity()"], "4": ["Choose activity", "app.choose_activity()"], "5": ["Display my activities", "app.display_user_activities()"]}
    while True:
        print()
        # print(f"\nUser list: {app.get_user_list()}\n")
        print(f"The current user is {Bcolors.OKBLUE}{Bcolors.BOLD}{app.get_cur_user(True)}{Bcolors.ENDC}")
        for a in action_list:
            print(f"{a:<3}: {action_list[a][0]}")
        action_num = input("\nChoose action from the list above: ")
        if action_num not in action_list:
            print(f"\n{Bcolors.FAIL}[ERROR]: Incorrect action number, try again\n{Bcolors.ENDC}")
            continue
        exec(action_list[action_num][1])
    
except KeyboardInterrupt:
    print(f"\n\n{Bcolors.WARNING}Aborted{Bcolors.ENDC}")
    print(f"{Bcolors.WARNING}App shutdown{Bcolors.ENDC}")