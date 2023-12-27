import random
from tabulate import tabulate
from worker import Worker

shifts = ["Opening", "Closing", "Mid"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# employees_ = ["Person{}".format(i) for i in range(1, 9)]
# num_employees = len(employees)
shift_requirements = {"Opening": 2,
                      "Closing": 3,
                      "Mid": 1}
def visualize_schedule(schedule):
    table_data = []
    for day in days:
        row = [day]
        for shift in shifts:
            display_row = [f"{value.name} ({value.role})" for value in schedule[day][shift]]
            row.append(", ".join(display_row))
        table_data.append(row)

    headers = ["Day"] + shifts
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def worker_generating():
    created_names = ["Person{}".format(i) for i in range(1, 9)]
    random.shuffle(created_names)
    employees = []
    store_off_days = []
    counter=0
    for employee in created_names:
        retry_off_days = True
        while retry_off_days:
            day_counter = random.randint(0, 5)
            if store_off_days.count(day_counter) >= 2:
                retry_off_days = True
                continue
            if counter == 0:
                role = "Head Supervisor"
            elif counter <=4:
                role = "Supervisor"
            else:
                role = "Barista"
            worker_instance = Worker(name=employee,role=role)
            worker_instance.set_weekly_days_off([days[day_counter],days[day_counter+1]])
            store_off_days.append(day_counter)
            retry_off_days = False
            # if day_counter==5:
            #     day_counter=0
            # else: 
            #     day_counter+=1
            employees.append(worker_instance)
            counter+=1  
            break   
    return [employees,employees[0]]

# Function to initialize an empty schedule
def initialize_schedule():
    return {day: {shift: [] for shift in shifts} for day in days}

def viable_worker(worker,schedule, day,shift):

    # Requirement 1: One supervisor and one barista
    if shift == "Opening":
        if len(schedule[day][shift]) != 0:
            if worker.role in schedule[day][shift][0].role:
                return False
    # Requirement 2: Not more than one supervisor at a time
    elif len(schedule[day][shift]) != 0 and shift in ["Mid","Closing"]:
       for key in schedule[day][shift]:
           if key.role == "Supervisor" and worker.role == "Supervisor":
               return False
    
    # Pass all required requirements
    if day not in worker.working_schedule and day not in worker.weekly_days_off and day not in worker.annual_leave_days:
        if (sum(shift in worker.working_schedule[key] for key in worker.working_schedule)) < 3:
            if schedule[day][shift] is None:
                return True
            elif len(schedule[day][shift]) + 1 <= int(shift_requirements[shift]):
                return True
    else:
        return False

def rank_workers(employees):
    workers_list = []
    for worker in employees:
        workers_list.append((worker,len(worker.working_schedule)))
    
    sorted_workers = sorted(workers_list, key=lambda item: item[1])
    return sorted_workers

def clean_up(schedule,sorted_employees):
    for worker,hours in sorted_employees:
        trials=0
        while trials<10:
            if (hours >= 5):
                break
            trials+=1
            for day in days:
                if day not in worker.working_schedule and day not in worker.weekly_days_off and day not in worker.annual_leave_days:
                    for shift in shifts:
                        if len(schedule[day][shift]) < int(shift_requirements[shift]):
                            schedule[day][shift].append(worker)
                            worker.work(day,shift)
                            hours = len(worker.working_schedule)
                            break

    return schedule
def generate_schedule():
    schedule = initialize_schedule()
    [employees,head_supervisor] = worker_generating()
    for day in days:
        for shift in shifts:
            if shift == "Mid" and day not in ("Saturday", "Sunday"):
                break
            # Shuffle employees to introduce randomness
            # Find the first available person who does not violate requirements
            trials=0
            while trials<5:
                if len(schedule[day][shift])>= int(shift_requirements[shift]):
                    break
                trials +=1
                random.shuffle(employees)
                for person in employees:
                    if shift == "Opening" and day not in head_supervisor.working_schedule and day not in head_supervisor.weekly_days_off and day not in head_supervisor.annual_leave_days:
                            schedule[day][shift].append(head_supervisor)
                            head_supervisor.work(day,shift)
                            break
                    # print("reached")
                    elif viable_worker(person,schedule, day, shift):
                        # print(person.name +" has been assigned for the Day: "+day+" and Shift: "+shift)
                        schedule[day][shift].append(person)
                        person.work(day,shift)
                        break
    sorted = rank_workers(employees)
    final_schedule = clean_up(schedule,sorted)
    sorted_workers = rank_workers(employees)
    return [final_schedule,sorted_workers]


def score_check(schedule,employees):
    points = 0
    for day in days:
        for shift in shifts:
            # Rule 1: Count Opening and Closing everyday
            if shift != "Mid" or day in ["Saturday", "Sunday"]:
                if len(schedule[day][shift]) <  int(shift_requirements[shift]):
                    points += -1

            # Rule 2: Measure how many workers are below 5 working days
            for worker,hours in employees:
                if hours < 5:
                    points += -1
    return points

def find_best(max_tries = 100):
    best_score = -100
    best_schedule = []
    best_employee = []
    for i in range (0,max_tries):
        [generated_schedule, sorted_workers] = generate_schedule()
        current_score = score_check(generated_schedule,sorted_workers)
        if current_score > best_score:
            best_score = current_score
            best_schedule = generated_schedule
            best_employee = sorted_workers
    # Visualize the generated schedule
    visualize_schedule(best_schedule)
    for employee,_ in best_employee:
        employee.print_details()
        print()

find_best(1000)