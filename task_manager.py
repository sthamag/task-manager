# Task Management System

''' 
This Python script implements a simple task management system with user authentication.
task creation, viewing, editing, and reporting functionalities. The system allows users
to log in, register new accounts, add tasks, view tasks, mark tasks as complete, edit
task details, generate reports on task and user overview, and display statistics on 
the number of users and tasks in the system.
'''

# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

def reg_user():
    '''Add a new user to the user.txt file'''

    # Request input of a new username
    while True:
        new_username = input("New Username: ")
        # Check if the username already exists
        if new_username in username_password:
            print("Username already exists. Please choose a different one.")
        else:
            break

    # Request input of a new password and confirm password
    while True:      
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same
        if new_password == confirm_password:
            # Add the new user to the user.txt file
            print("New user added")
            username_password[new_username] = new_password
            
            # Write the updated user data to the user.txt file
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            
            break # break out of the loop when the password match
        else:
            print("Passwords do no match")

def add_task(task_list):
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.'''
    
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break
        
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Get the current date.
    curr_date = date.today()

    # Add the data to the task list.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)

    # Write the updated task list to the file tasks.txt.
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for task in task_list:
            str_attrs = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

    print("Task successfully added.")

def view_all(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''

    for index, task in enumerate(task_list):
        print_task(task, index)

def view_mine(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    '''
    
    user_tasks = [task for task in task_list if task['username'] == curr_user]
    
    for index, task in enumerate(user_tasks):
        print_task(task, index)


    task_selection = input("Enter the number of the task you want to select, or enter -1 to return to the main menu: ")

    if task_selection == '-1':
        print("Returning to the main menu...")
        return
    else:
        try:
            # Retrieve the selected task
            task_index = int(task_selection) - 1

            if 0 <= task_index < len(task_list):
                selected_task = user_tasks[task_index]

                # Create a formatted string for the selected task and display
                selected_task_str = f"Task: \t\t {selected_task['title']}\n"
                selected_task_str += f"Assigned to: \t {selected_task['username']}\n"
                selected_task_str += f"Date Assigned: \t {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                selected_task_str += f"Due Date: \t {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                selected_task_str += f"Task Description: \n {selected_task['description']}\n"
                print(f"You selected task {task_index + 1}:")
                print(selected_task_str)
                
                # Check if the task is already completed
                if selected_task["completed"]:
                    print("This task has already been completed.")
                else:
                    #Prompt the user to mark the task or do edits
                    mark_task = input("Would you like to mark this task as complete? (yes/no): ").strip().lower()
                    if mark_task == "yes":
                        selected_task["completed"] = True
                        print(f"This task has been marked complete.")
                        print(selected_task_str)
                    elif mark_task == "no":
                        if selected_task["completed"]:
                            print("This task has already been completed hence, cannot be edited.")
                        else:
                            edit_task = input("Would you like to edit this task? (yes/no): ").strip().lower()
                            if edit_task == "yes":
                                edit_option = input("What would you like to edit? (username/due date):  ").strip().lower()
                                if edit_option == "username":
                                    new_user = input("Enter the new username for this task: ")
                                    if new_user in username_password:
                                        user_tasks[task_index]["username"] = new_user
                                        print(f"Task reassigned to {new_user}.")    
                                    else:
                                        print("Username not found. Please enter a valid username.")                      
                                elif edit_option == "due date":
                                    try:
                                        new_date = input("Enter the new due date of task (YYYY-MM-DD): ")
                                        new_date_time = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                                        user_tasks[task_index]["due_date"] = new_date_time
                                        print("Due date successfully updated.")
                                    except ValueError:
                                        print("Invalid datetime format. Please use the format specified.")
                                else:
                                    print("Invalid input. Please enter username or due date.")                        
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid task number.")

    # Write the updated task list to the file tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
        

def print_task(task, index):
    '''Prints the details of a task along with its index'''
    # Create a formatted string containing task details
    disp_str = f"Task: \t\t {task['title']}\n"
    disp_str += f"Assigned to: \t {task['username']}\n"
    disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Description: \n {task['description']}\n"

    # Print the index of the task along with its details
    print(str(index + 1) + ". " + disp_str)

def generate_task_overview(task_list):
    '''Generates an task overview and writes it to task_overview.txt'''
    
    # Count total tasks, completed tasks and uncompleted tasks 
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    current_date = datetime.now().date()

    # Count overdue uncompleted tasks
    overdue_uncompleted_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < current_date)
    
    # Calculate percentage of uncompleted tasks and percentage of overdue uncompleted tasks
    percentage_uncompleted = (uncompleted_tasks / total_tasks) * 100
    percentage_overdue = (overdue_uncompleted_tasks / uncompleted_tasks) * 100

    # Write the overview to task_overview.txt
    with open("task_overview.txt", "w") as file:
        file.write("Task Overview\n")
        file.write("-------------------------------\n")
        file.write(f"Total number of tasks: {total_tasks}\n")
        file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        file.write(f"Total number of overdue uncompleted tasks: {overdue_uncompleted_tasks}\n")
        file.write(f"Percentage of uncompleted tasks: {percentage_uncompleted: .2f}%\n")
        file.write(f"Percentage of overdue completed tasks: {percentage_overdue: .2f}%\n")
    

def generate_user_overview(user_data, task_list):
    '''Generates an user overview and their tasks and writes it to user_overview.txt'''

    # Count total number of users and total number of tasks
    total_users = len(user_data)
    total_tasks = len(task_list)

    # Write the user overview to user_overview.txt
    with open("user_overview.txt", "w") as file:
        file.write("User Overview\n")
        file.write("--------------------------------\n")
        file.write(f"Total number of users registered: {total_users}\n")
        file.write(f"Total number of tasks generated: {total_tasks}\n\n")
        file.write("User\tTotal Tasks\t\t% of Total Tasks\t% of Completed Tasks\t% of Incomplete Tasks\t% of Overdue Incomplete Tasks\n")

        for username in username_password:
            user_tasks = [task for task in task_list if task['username'] == username]
            total_user_tasks = len(user_tasks)

            # Calculate percentages related to the user's tasks
            percentage_total_user_tasks = (total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            completed_user_tasks = sum(1 for task in user_tasks if task['completed'])
            percentage_completed_user_tasks = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            incomplete_user_tasks = total_user_tasks - completed_user_tasks

            if incomplete_user_tasks > 0:
                current_date = datetime.now().date()
                overdue_uncompleted_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'].date() < current_date)
                percentage_overdue_incomplete_tasks = (overdue_uncompleted_tasks / incomplete_user_tasks) * 100
            else:
                percentage_overdue_incomplete_tasks = 0
            
            # Write the user's overview data to the file
            file.write(f"{username}\t\t{total_user_tasks}\t\t\t\t{percentage_total_user_tasks:.2f}%\t\t\t\t\t"
                       f"{percentage_completed_user_tasks:.2f}%\t\t\t\t\t{(100 - percentage_completed_user_tasks):.2f}%\t\t\t\t\t"
                       f"{percentage_overdue_incomplete_tasks:.2f}%\n")

def create_taskfile():
    '''Creates tasks.txt if it doesn't exist.'''

    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8"):
            pass

def create_userfile():
    '''Create users.txt file with default admin credentials if it doesn't exist.'''

    if not os.path.exists("user.txt"):
        with open("user.txt", "w", encoding="utf-8") as default_file:
            default_file.write("admin;password")

def display_stats():
    '''
    The 'display_stats' function reads the number of users and tasks from text files and displays
    the statistics.
    '''

    # Ensure that user.txt and tasks.txt files exist
    create_userfile()
    create_taskfile()

    try:
        with open("user.txt", "r", encoding="utf-8") as users:
            num_users = sum(1 for _ in users)
    except FileNotFoundError:
        # If user.txt doesn't exist, set the number of users to 0
        num_users = 0

    try:
        with open("tasks.txt", "r", encoding="utf-8") as tasks:
            num_tasks = sum(1 for _ in tasks)
    except FileNotFoundError:
        # If tasks.txt doesn't exist, set the number of tasks to 0
        num_tasks = 0

    # Display the statistics
    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")  

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics (only accessible to admin)
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()     

    elif menu == 'a':
        add_task(task_list)

    elif menu == 'va':
        view_all(task_list)

    elif menu == 'vm':
        view_mine(task_list)

    elif menu == 'gr':
        generate_task_overview(task_list)
        generate_user_overview(user_data, task_list)
        print("Reports generated in local directory.")
    
    elif menu == 'ds':
        if curr_user == 'admin': 
            display_stats()
        else:       
            print("To display statistics, you need to be an administrator.") 

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")