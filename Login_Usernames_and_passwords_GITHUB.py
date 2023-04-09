import sqlite3

# Firstly lets create a connection to the database.

conn = sqlite3.connect('Database name here')

# Create a table to store the user accounts.

conn.execute('''
CREATE TABLE IF NOT EXISTS (Database name here)
(username TEXT PRIMARY KEY,
 password TEXT NOT NULL)
''')

# Lets create our class for our nodes.

class Node:
    def __init__(self, data=None):
        self.data = data

#This function is pretty much the heart of the code it can create accounts and store them while also confirming they have an account.

def User_Account_Creation():

    # Lets create our nodes here. Node1 either logs the user in or signs them up. node3 sends them to where the can create an account.
    #I also added a limit on the characters in the user's password in node3 it sets to 10 - 13 characters.

    node1 = Node(input("Hello welcome to Solo's computer. If you already have an account, type login. If not, type sign up: "))
    if node1.data == "sign up":
        node3 = Node(input(f"What would you like your username to be? "))
        print(f'Your username is now {node3.data}!!!')
        while True:
            password = input("Please create a strong password: ")
            if len(password) < 10 or len(password) > 13:
                print("Password should be between 10 to 13 characters long.")
            elif not any(char.isdigit() for char in password):
                print("Password should contain at least one digit.")
            elif not any(char.isupper() for char in password):
                print("Password should contain at least one uppercase letter.")
            else:
                print("Password created successfully!")
                break
        # Ok here we insert the information(username and password) to the database.
        #To add to that node5 can either exit the function or recursivelly call the function sending the user back to the login or sign up options.

        conn.execute('INSERT INTO user_accounts2 (username, password) VALUES (?, ?)', (node3.data, password))
        conn.commit()
        node5 = Node(input(f"Congratulations on creating your account! Would you like to return to the login or quit? "))
        if node5.data == "login":
            return User_Account_Creation()
        else:
            exit()

#Here I create a collection of if statements in while loop. 
#This while loop gives the user the options to create account using recurssion or log the user in and confirming their account exists!
    else:
        while node1.data == "login":
            username = input(f"Enter your username or if you don't have a account type sign up: ")
            if username.lower() == "sign up":
                User_Account_Creation()
                break
            elif username == username:
                    password = input(f'Enter your password: ')
                    # This check if the username and password are in the database
                    cursor = conn.execute('SELECT username FROM (DATABASE NAME HERE) WHERE username=? AND password=?', (username, password))
                    if cursor.fetchone() != None:
                         return print(f"Hello welcome to your account {username} :) ")
                    else:
                        print('Invalid username or password') 
                    # If the Username and password are valid, will print a return statement.
                    # If not either the username or passwor is invalid.

# Lets call our function here!
start_node = User_Account_Creation()
print(start_node)