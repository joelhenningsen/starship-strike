"""Program: main.py

Author: Joel Henningsen
Date Completed: 06/14/2023

This module runs code from the menu module to create an instance of the MainMenu 
class in the menu module, and then use one of that classes functions to run the menu.
Libraries that must be installed in order to run this program are: random, pygame

Run main.py to start the program.
"""


from menu import MainMenu

 
def main():
    # Initializing object from Class and calling run function
    menu = MainMenu()
    menu.run()

if __name__ == "__main__":
    main()
  