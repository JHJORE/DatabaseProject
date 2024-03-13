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
    
    print("""
        1. Initialize Database and Insert Initial Data
        2. Insert Sold Chairs from Files
        3. Buy Tickets
        4. List Performances by Date
        5. List Actors by Play
        6. Performances by Ticket Sales
        7. Find Co-actors
        8. Exit
        """)

    choice = input("Enter your choice: ")


    if choice == '1':
        database.initialize_db()

    elif choice == '2':
            # Insert sold chairs from files
        pass
    elif choice == '3':
        # Implement buying tickets logic
        pass
    elif choice == '4':
        # List performances by date
        pass
    elif choice == '5':
        # List actors by play
        pass
    elif choice == '6':
        # List performances by ticket sales
        pass
    elif choice == '7':
        # Find co-actors for a given actor
        pass
    elif choice == '8':
        print("Exiting...")
        time.sleep(2)
        clear_screen()
    else:
        print("Invalid choice. Please choose again.")

def manage_theater_halls():
    
    print("Theater Hall Management")
  
def manage_plays():
    
    print("Play Management")
    

def manage_employees():
    
    print("Employee Management")
    