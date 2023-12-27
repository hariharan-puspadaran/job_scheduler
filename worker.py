class Worker:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.weekly_days_off = None
        self.working_schedule = {}  # Dictionary to store days and shifts worked in the current week
        self.annual_leave_days = set()

    def set_weekly_days_off(self, days_off):
        # Assuming `days_off` is a list of two consecutive days (e.g., ["Monday", "Tuesday"])
        self.weekly_days_off = days_off

    def work(self, day, shift):
        if day not in self.working_schedule:
            self.working_schedule[day] = {shift}
        # self.working_schedule[day][shift] = True

    def take_annual_leave(self, day):
        self.annual_leave_days.add(day)

    def print_details(self):
        print("Name: " + self.name)
        print("Role: " + self.role)
        print("Weekly Days Off: " + ", ".join(self.weekly_days_off))
        print("Number of work days: " + str(len(self.working_schedule)))


    def __repr__(self):
        return f"{self.name}"

# # Example usage
# worker1 = Worker("Person1")
# worker1.set_weekly_days_off(["Saturday", "Sunday"])
# worker1.work("Monday", "Mid")
# worker1.work("Tuesday", "Mid")
# worker1.take_annual_leave("Wednesday")
# closing_count = sum("Mid" in worker1.working_schedule[key] for key in worker1.working_schedule)
# print(closing_count)



# # Print worker data
# print(f"{worker1.name}: Weekly days off: {worker1.weekly_days_off}, Working schedule: {worker1.working_schedule}, Annual leave days: {worker1.annual_leave_days}")
