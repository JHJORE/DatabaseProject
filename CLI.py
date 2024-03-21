import os
import time
import subprocess
import database

def clear_screen():
    # For Windows
    if os.name == 'nt':
        subprocess.run(['cls'], shell=True, check=True)
    # For macOS and Linux
    else:
        subprocess.run(['clear'], shell=True, check=True)

def main_menu():
    logged_off = False
    while not logged_off:
        print("""
            1. Initialize Database and Insert Initial Data
            2. Insert data
            3. Check Chair Availability
            4. Buy Tickets
            5. Find Actors by Play by date
            6. What actors are playing in a given play
            7. Most popular play
            8. Find co-actors for a given actor
            9. Exit
            """)

        choice = input("Enter your choice: ")


        if choice == '1':
            database.initialize_db()
            database.fill_db()
            clear_screen()

        elif choice == '2':
                # Insert data
            pass
        elif choice == '3':
            # Implement check chair
            pass
        elif choice == '4':
            # Buy Tickets
            pass
        elif choice == '5':
            # Find actors by play by date
            pass
        elif choice == '6':
            # List What actors are playing in a given play
            pass
        elif choice == '7':
            # Most popular play
            # 8. Find co-actors for a given actor for a given actor
            pass
        elif choice == '8':
            # Most popular play
            # 8. Find co-actors for a given actor for a given actor
            pass
        elif choice == '9':
            print("Exiting...")
            logged_off = True
        else:
            print("Invalid choice. Please choose again.")

def manage_theater_halls():
    
    print("Theater Hall Management")
  
def manage_plays():
    
    print("Play Management")
    

def manage_employees():
    
    print("Employee Management")
    