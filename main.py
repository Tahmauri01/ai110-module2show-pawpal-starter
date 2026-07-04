from pawpal_system import Task, Owner, Schedule

# Create owner
owner = Owner(owner_id=1, name="Alex Rivera")

# Add two pets
buddy = owner.add_pet(name="Buddy", age=3, breed="Golden Retriever")
luna  = owner.add_pet(name="Luna",  age=5, breed="Siamese Cat")
john = owner.add_pet(name = "John", age = 20, breed = "Human")
mill = owner.add_pet(name = "Mill", age = 2, breed = "hamster")


# Add three tasks across the pets with different times and days



buddy.tasks.append(Task(
    task_id=1,
    name="Morning Walk",
    time="07:30",
    priority=3,
    frequency=[1, 3, 5],        # Mon, Wed, Fri
    description="30-minute walk around the park",
))

buddy.tasks.append(Task(
    task_id=2,
    name="Evening Feeding",
    time="18:00",
    priority=2,
    frequency=[1, 2, 3, 4, 5, 6, 7],  # Every day
    description="One cup of dry kibble",
))

luna.tasks.append(Task(
    task_id=1,
    name="Grooming",
    time="10:00",
    priority=1,
    frequency=[6, 7],           # Sat, Sun
    description="Brush coat and trim nails",
))

john.tasks.append(Task(
    task_id=3,
    name = "eat",
    time="16:00",
    priority="low",
    frequency= [6],
    description="Has to be fed every week",
))

mill.tasks.append(Task(
    task_id=3,
    name = "run",
    time="19:00",
    priority="low",
    frequency= [6],
    description="Has to run every week",
))

# Build and print the schedule
schedule = Schedule(schedule_id=1, date="2026-07-02", owner=owner)
schedule.generate_schedule()

print(f"\nSchedule for {owner.name}:")
schedule.view_schedule()
schedule.update_schedule()

