import random
import copy

# Constants
shifts = ["Opening", "Mid", "Closing"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
num_supervisors = 3
num_baristas = 5
num_people = num_supervisors + num_baristas

# Generate initial population
def generate_schedule():
    return {
        day: {
            shift: None
            for shift in shifts
        }
        for day in days
    }

def initialize_population(population_size):
    return [generate_schedule() for _ in range(population_size)]

# Fitness function
def fitness(schedule):
    # Rule 1: Each worker needs 2 days off
    for person in range(1, num_people + 1):
        worked_days = [day for day_shifts in schedule.values() for shift_workers in day_shifts.values() if shift_workers and person in shift_workers]
        off_days = set(days) - set(worked_days)
        if len(off_days) < 2:
            return -1  # Penalize schedules with workers not getting 2 days off

    # Rule 2: Morning shift needs 1 supervisor and 1 barista
    for day in days:
        if schedule[day]["Opening"] is not None:
            supervisor_count = sum(1 for person in schedule[day]["Opening"] if person and person.startswith("Supervisor"))
            barista_count = sum(1 for person in schedule[day]["Opening"] if person and person.startswith("Barista"))
            if supervisor_count != 1 or barista_count != 1:
                return -1  # Penalize schedules with incorrect morning shift composition
    # Rule 4: Each worker can work the same shift at most three times
    shift_counts = {person: {shift: 0 for shift in shifts} for person in range(1, num_people + 1)}
    for day_shifts in schedule.values():
        for shift, workers in day_shifts.items():
            if workers is not None:
                for worker in workers:
                    shift_counts[worker][shift] += 1

    for person, shift_counts_per_person in shift_counts.items():
        for shift, count in shift_counts_per_person.items():
            if count > 3:
                return -1  # Penalize schedules where a worker works the same shift more than three times
    # # Rule 3: The head supervisor will work each morning other than the 2 days off they have for the week
    # head_supervisor = "Supervisor1"  # Adjust based on your worker naming
    # off_days = set(days) - set(schedule[head_supervisor]["Opening"]) if schedule[head_supervisor]["Opening"] else set()
    # if len(off_days) != 2:
    #     return -1  # Penalize schedules where the head supervisor is not scheduled for the morning shift on the correct days

    # Your additional rules can be added here

    # If all rules are satisfied, return a positive fitness score
    return sum(sum(1 for shift_workers in day_shifts.values() if shift_workers is not None) for day_shifts in schedule.values())


# Genetic operators
def crossover(parent1, parent2):
    child = copy.deepcopy(parent1)
    for day in days:
        for shift in shifts:
            if random.random() < 0.5:
                child[day][shift] = parent1[day][shift]
            else:
                child[day][shift] = parent2[day][shift]
    return child

def mutate(schedule):
    mutated_schedule = copy.deepcopy(schedule)
    day = random.choice(days)
    shift = random.choice(shifts)
    mutated_schedule[day][shift] = random.sample(range(1, num_people + 1), 2)
    return mutated_schedule

# Genetic algorithm
def genetic_algorithm(population_size, generations):
    population = initialize_population(population_size)

    for generation in range(generations):
        # Evaluate fitness for each schedule in the population
        fitness_scores = [fitness(schedule) for schedule in population]

        # Check if all fitness scores are negative
        if all(score < 0 for score in fitness_scores):
            print("All schedules have negative fitness. Returning a default schedule.")
            return generate_schedule()

        # Select parents based on fitness scores (roulette wheel selection)
        parents = random.choices(population, weights=fitness_scores, k=2)

        # Crossover to create children
        child = crossover(parents[0], parents[1])

        # Mutate child
        mutated_child = mutate(child)

        # Replace the least fit schedule in the population with the mutated child
        min_fitness_index = fitness_scores.index(min(fitness_scores))
        population[min_fitness_index] = mutated_child

        print(f"Generation {generation + 1}, Best Fitness: {max(fitness_scores)}")

    # Return the best schedule found
    best_schedule = max(zip(population, fitness_scores), key=lambda x: x[1])[0]
    return best_schedule
    population = initialize_population(population_size)

    for generation in range(generations):
        # Evaluate fitness for each schedule in the population
        fitness_scores = [fitness(schedule) for schedule in population]

        # Select parents based on fitness scores (roulette wheel selection)
        parents = random.choices(population, weights=fitness_scores, k=2)

        # Crossover to create children
        child = crossover(parents[0], parents[1])

        # Mutate child
        mutated_child = mutate(child)

        # Replace the least fit schedule in the population with the mutated child
        min_fitness_index = fitness_scores.index(min(fitness_scores))
        population[min_fitness_index] = mutated_child

        print(f"Generation {generation + 1}, Best Fitness: {max(fitness_scores)}")

    # Return the best schedule found
    best_schedule = max(zip(population, fitness_scores), key=lambda x: x[1])[0]
    return best_schedule

# Example usage
best_schedule = genetic_algorithm(population_size=50, generations=100)
print("\nBest Schedule:")
for day in days:
    print(f"{day}:")
    for shift in shifts:
        print(f"  {shift}: {best_schedule[day][shift]}")
