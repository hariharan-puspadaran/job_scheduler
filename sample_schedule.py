import random
from tabulate import tabulate
from worker import Worker


# Constants
shifts = ["Opening", "Mid", "Closing"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
employees = ["Person{}".format(i) for i in range(1, 9)]
num_employees = len(employees)
shift_requirements = {"Opening": "1",
                      "Mid": "1",
                      "Closing": "2"}




# Function to initialize an empty schedule
def initialize_schedule():
    return {day: {shift: None for shift in shifts} for day in days}

# Function to check if adding a person to a shift violates requirements
# Updated function to check if adding a person to a shift violates requirements
def violates_requirements(schedule, day, shift, person):

    # Requirement 1: Same worker can't work twice in a day
    if person in schedule[day].values():
        print(person + " is on this schedule for " + day+" and current shift: "+shift)
        for value in schedule[day].values():
            print(value)
        # Requirement 2: Each worker needs 2 days without any work in the week
        days_without_work = sum(1 for d in days if schedule[d][shift] is None and person not in schedule[d].values())
        if days_without_work >= 2:
            # Additional check for existing violations
            max_count = shift_requirements[shift]
            if schedule[day][shift] != None and schedule[day][shift].count() + 1 > max_count:
                return True
            # for count in shift_requirements[shift].items():
                



            #     if schedule[day][shift].count(role) + (person == role) > count:
            #         return True    
    return False


# Greedy algorithm for scheduling
def generate_schedule():
    schedule = initialize_schedule()
    
    for day in days:
        for shift in shifts:
            # Shuffle employees to introduce randomness
            random.shuffle(employees)
            # Find the first available person who does not violate requirements
            for person in employees:
                if schedule[day][shift] is None and not violates_requirements(schedule, day, shift, person):
                    print(person+" has been assigned for the Day: "+day+" and Shift: "+shift)
                    schedule[day][shift] = person
                    break
    
    return schedule

# Function to visualize the schedule as a table
def visualize_schedule(schedule):
    table_data = []
    for day in days:
        row = [day]
        for shift in shifts:
            row.append(schedule[day][shift])
        table_data.append(row)

    headers = ["Day"] + shifts
    print(tabulate(table_data, headers=headers, tablefmt="grid"))



# Print the generated schedule
generated_schedule = generate_schedule()
# for day in days:
#     print(f"{day}:")
#     for shift in shifts:
#         print(f"  {shift}: {generated_schedule[day][    shift]}")

# Visualize the generated schedule
visualize_schedule(generated_schedule)
