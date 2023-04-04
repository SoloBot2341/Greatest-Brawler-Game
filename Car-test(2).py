import time
import threading

Map = {
    "icecream shop": 10,
    "library": 12,
    "energy station": 5,
    "museum": 30,
    "home": 0,
    "mcdonald": 22,
    "jo's barbershop": 17,
    "park": 8,
    "funkin donut": 15,
    "amc theater": 25
}

distances = (float(value) for value in Map.values())
destinations = list(Map.keys())
default_energy = 100
distance = 0
destination = 0
current_energy = default_energy
Gain_energy = 0

class Energy:
    def __init__(self, energy_management):
        self.energy = energy_management

def Max_energy():
    global energy_used_total
    global energy_used 
    global current_energy
    global Gain_energy
    global destination

    energy_used = [default_energy - dist for dist in distances]
    while True:
        Gain_energy = input("""your current energy level is """ + str(default_energy) + ' units'
                           """ How many units of energy would you like to add? NOTE(MAX = 150): """)
                               
        current_energy = default_energy + float(Gain_energy)
        while True:
           if float(Gain_energy) > 150:
                print("Remember the limit is 150 units of energy!")
           else:
                Gain_energy = float(Gain_energy)
                energy_used_total = sum(energy_used + [Gain_energy])
                print("You've arrived at the energy station current amount of energy is", current_energy, "units")
                print(f"You've added {Gain_energy} units of energy!")
                return current_energy
        

        

def Timer(Map):
    global trip_time
    global current_energy
    global destination

    while True:
        mph = float(input("How fast would you like to get there? Note(speed limit = 150mph and you can't go faster than 3 times your destination distance!): "))
        if mph > int(Map[destination]) * 3 or mph > 150:
            print("WOAH that's too fast! Are you trying to get a ticket???")
        else:
            trip_time = int(Map[destination] / mph)
            hours, remaining_seconds = divmod(trip_time * 3600, 3600)
            minutes, seconds = divmod(remaining_seconds, 60)
            print(f"Your trip is now starting. It will take approximately {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds to arrive there.")
            start_time = f"{int(hours)}, {int(minutes)}, {int(seconds)}"

            time_remaining = trip_time * 3600

            while time_remaining > 0:
                hours, remaining_seconds = divmod(time_remaining, 3600)
                minutes, seconds = divmod(remaining_seconds, 60)
                print(f"Time remaining: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
                time.sleep(1)  # Wait for 1 second before updating the timer
                time_remaining -= 1

            print("You have arrived at your destination")
            break

def Trips(Map):
    global trip_time
    global distance
    global destinations
    global current_energy
    global destination
    valid_destinations = ', '.join(Map.keys())
    distance = (float(value) for value in Map.values())
    while True:
        destination = input(f'All safety requirements met! Where would you like to go? {Map}: ')
        if destination.lower() in Map:
            print(f"Your current energy level is {current_energy} units this trip will cost you {Map[destination]}  units!")
            Timer(Map)
            Other_trip()
            break
        else:
            print('Please enter a valid destination')
    if destination == "energy station":
        Timer(Map)
        Max_energy()
        return current_energy






def Other_trip():
    Another_trip = input("Would you like to start another trip?: (yes/no) ")
    if Another_trip.lower() == "yes":
        Trips(Map)
    elif Another_trip.lower() == "no":
        Turn_off_or_not = input("Would you like to turn off the car?: (off/stay on)")
        if Turn_off_or_not == "off":
            exit()
        else:
            Trips(Map)
            return
    
        

Trips(Map)
