import time

class Oven:
    def __init__(self, timer, username, temperature, mode="off"): 
        self.timer = timer
        self.username = username
        self.tempature = temperature
        self.mode = mode

        
# this function turns the oven on. If the user inputs "off" the program closes"
def get_mode(self):
        if self.mode == "on":
            return "Oven now on"
        else:
            return "Oven off"



def username():
    username = (input("Create a username "))
    print("Great your username is " + str(username) + " Welcome to solo's Oven ")
    return username

 #This functions checks if the user turned the oven on or off. If the oven is turned on it runs the username function.       
def mode():
    mode = input("enter oven mode (on/off): ")
    if mode == "on":
         username()
    else:
         mode == "off"
         exit()
    return mode




def temperature():
    while True:
        temp_str = input("What should the temperature be?: ")
        try:
            temp = int(temp_str)
            if temp < 1 or temp > 500:
                print("Please input a valid temperature between 1 and 500.")
            else:
                answer = input("Are you sure you want the temperature to be " + str(temp) + "F? (yes/no)")
                if answer == "yes":
                    print("Great, oven is now " + str(temp) + "F")
                    break
                elif answer == "no":
                    print("OK, what would you like the temperature to be?")
                else:
                    print("Please answer 'yes' or 'no'")
        except ValueError:
            try:
                temp = float(temp_str)
                print("Please input a valid temperature as a whole number between 1 and 500.")
            except ValueError:
                print("Please input a valid temperature as a whole number between 1 and 500.")
#Here I created a time function were it checks for real numbers and makes countdown based on the user's input. This was easily the most difficult function to create. 
def timer():
    while True:
        try:
            run_time = float(input("How long do you want to cook your meal?: "))
            if run_time <= 0:
                print('Please pick a valid time to start the timer.')
            else:
                start_time = time.time()
                while True:
                    elapsed_time = time.time() - start_time
                    remaining_time = run_time - elapsed_time
                    if remaining_time <= 0:
                        print('Ding! Time is up, your meal is ready!')
                        return True
                    print('Time remaining: {:.0f} seconds'.format(remaining_time))
                    time.sleep(1)
                break
        except ValueError:
            print("Please input a valid time as a number greater than 0.")
            


Solo_oven =(mode(),temperature(),timer())

Counter = timer() <= 0

def Further_options():
    if Counter:
        option1 = input("Would you like to cook another meal or shut down: yes/no")
        return
    
Further_options()





      
    



