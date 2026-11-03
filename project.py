### final project of week 9

import csv
import os



def main():
    sessions = load_sessions()
    while True:
        print("Study Time Tracker")
        menu = input("""Choose an option:
1. Add a study session
2. View total time
3. View average time
4. Check a goal
5. Quit
""")
        
        if menu == '1':
            new_session = get_session()
            sessions.append(new_session)
            save_sessions([new_session])
            continue
        
        elif menu == '2':
            time = calculate_total(sessions)
            subjects = group_by_subject(sessions)
            print(f"Total study time: {time} minutes")
            print("Study time by subject:")
            for subject, duration in subjects.items():
                print(f"  {subject}: {duration} minutes")
            continue
        
        elif menu == '3':
            total = calculate_total(sessions)
            average = calculate_average(total, 7)
            print(f"Average study time: {average:.2f} minutes")
            continue
        
        elif menu == '4':
            goal_subjects = input("Which subject you want to check? ")
            goals = load_goals()
            
            if goal_subjects not in goals:
                print(f'You haven\'t set a goal for this subject yet.')
                try:
                    goal_minutes = int(input("Enter your study goal in minutes: "))
                except ValueError:
                    print("Invalid input. Please enter a valid number for the goal.")
                    continue
                
                save_goal(goal_subjects, goal_minutes)
                
            else:
                goal_minutes = goals[goal_subjects]
                print(f"You have set a goal for {goal_subjects} is {goal_minutes} minutes.")
                
            subjects = group_by_subject(sessions)
            actual = subjects.get(goal_subjects, 0)
                
            goal_met, remaining_time = check_goal(actual, goal_minutes)
            if goal_met:
                print("Congratulations! You've met your study goal.")
            else:
                print(f"You need {remaining_time} more minutes to reach your goal.")

        elif menu == '5':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a valid option from the menu.")
            continue



    
# to get the subject and dusation from the user
def get_session():
    subject = input("Enter the subject you studied: ")
    while True:
        try:
            duration = int(input("Enter the duration in minutes: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the duration.")
            
    return {'subject': subject, 'duration': duration}


# to calculate the total time of all sessions
def calculate_total(sessions):
    total_time = 0
    for session in sessions:
        total_time += session['duration']
    return total_time
    
    
# to calculate the average study time per day in a week
def calculate_average(total_minutes, days):
    if days <= 0:
        return 0
    return total_minutes / days
        
    
# to check if the user has met their study goal
def check_goal(actual_minutes, goal_minutes):
    if goal_minutes <= actual_minutes:
        return True, 0
    else:
        return False, goal_minutes - actual_minutes
  
    
# to load previous study sessions from a CSV file
def load_sessions():
    sessions = []
    try:
        with open('study_log.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                sessions.append({'subject': row['subject'], 'duration': int(row['duration'])})
    except FileNotFoundError:
        print("No previous study sessions found. Starting fresh.")
        return []         
    
    return sessions            
                
                        
# to save new study sessions to a CSV file
def save_sessions(sessions):
    file_exists = os.path.isfile('study_log.csv')
    with open('study_log.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['subject', 'duration'])
        
        if not file_exists:
            writer.writeheader()
        for session in sessions:
            writer.writerow({'subject': session['subject'], 'duration': session['duration']})

    
    
# to group study sessions by subjects
def group_by_subject(sessions):
    subjects = {}
    for session in sessions:
        subject = session['subject']
        duration = session['duration']
        if subject in subjects:
            subjects[subject] += duration
        else:
            subjects[subject] = duration
    return subjects


# to save study goals to a CSV file
def save_goal(subject, goal_minutes):
    file_exists = os.path.isfile('goals.csv')
    with open('goals.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['subject', 'goal_minutes'])
                
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({'subject': subject, 'goal_minutes': goal_minutes})
        


# to load study goals from a CSV file
def load_goals():
    goals = {}
    try:
        with open('goals.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                goals[row['subject']] = int(row['goal_minutes'])
    except FileNotFoundError:
        print("No previous study goals found. Starting fresh.")
        return {}  
        
    return goals            





if __name__ == "__main__":
    main()