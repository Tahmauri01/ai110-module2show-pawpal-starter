PRIORITY_LABELS = {1: "Low", 2: "Medium", 3: "High"}
FREQUENCY_DAYS = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
ALL_DAYS = set(FREQUENCY_DAYS.keys())

def _format_time(time_str):
    """Convert a 24-hour HH:MM string to a 12-hour AM/PM formatted string."""
    hour, minute = map(int, time_str.split(":"))
    period = "AM" if hour < 12 else "PM"
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12
    return f"{display_hour}:{minute:02d} {period}"

class Task:
    def __init__(self, task_id, name, time, priority, frequency, description, is_daily=False, is_complete=False):
        self.task_id = task_id
        self.name = name
        self.time = time
        self.priority = priority
        self.frequency = frequency
        self.description = description
        self.is_daily = is_daily
        self.is_complete = is_complete


    def mark_complete(self):
        """Mark this task as complete and append [COMPLETED] to its name."""
        self.is_complete = True
        self.name += " [COMPLETED]"
        #TODO: make completed status only appear on whichever status was chosen for that specific day

    def mark_daily(self):
        """Mark this task as daily so it appears on every day of the schedule."""
        self.is_daily = True

    def view_task_details(self):
        """Print all details of the task including time, frequency, priority, and completion status."""
        formatted_time = _format_time(self.time)

        priority_label = PRIORITY_LABELS.get(self.priority, str(self.priority))

        frequency_label = ", ".join(FREQUENCY_DAYS.get(d, str(d)) for d in self.frequency)

        print(f"Task:        {self.name}")
        print(f"Description: {self.description}")
        print(f"Time:        {formatted_time}")
        print(f"Frequency:   {frequency_label}")
        print(f"Priority:    {priority_label}")
        print(f"Complete:    {self.is_complete}")
        print(f"Daily:       {self.is_daily}")

    def update_task(self, name=None, time=None, priority=None, frequency=None, description=None):
        """Update any combination of the task's name, time, priority, frequency, or description."""
        if name is not None:
            self.name = name
        if time is not None:
            self.time = time
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency
        if description is not None:
            self.description = description


class Pet:
    def __init__(self, pet_id, name, owner_id, age, breed):
        self.pet_id = pet_id
        self.name = name
        self.owner_id = owner_id
        self.age = age
        self.breed = breed
        self.tasks = []

    def update_pet(self, name=None, age=None, breed=None):
        """Update any combination of the pet's name, age, or breed."""
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if breed is not None:
            self.breed = breed

    def view_pet_details(self, owner):
        """Print the pet's name, age, breed, and the name of its owner."""
        print(f"Name:  {self.name}")
        print(f"Age:   {self.age}")
        print(f"Breed: {self.breed}")
        print(f"Owner: {owner.name} (ID: {self.owner_id})")

    def view_pet_tasks(self):
        """Print the full details of every task assigned to this pet."""
        if not self.tasks:
            print(f"{self.name} has no tasks.")
            return
        print(f"Tasks for {self.name}:")
        for i, task in enumerate(self.tasks, start=1):
            print(f"\n  Task {i}:")
            task.view_task_details()


class Owner:
    def __init__(self, owner_id, name):
        self.owner_id = owner_id
        self.name = name
        self.pets = []

    def add_pet(self, name, age, breed):
        """Create a new Pet tied to this owner and add it to the owner's pet list."""
        pet_id = len(self.pets) + 1
        new_pet = Pet(pet_id, name, self.owner_id, age, breed)
        self.pets.append(new_pet)
        return new_pet

    def remove_pet(self, pet_id):
        """Remove the pet with the given pet_id from the owner's pet list."""
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def update_owner(self, name=None, add_pet=None, remove_pet_id=None):
        """Update the owner's name or add/remove a pet by calling add_pet() or remove_pet()."""
        if name is not None:
            self.name = name
        if add_pet is not None:
            self.add_pet(add_pet["name"], add_pet["age"], add_pet["breed"])
        if remove_pet_id is not None:
            self.remove_pet(remove_pet_id)

    def view_owner_details(self):
        """Print the owner's name and ID, then list all their pets."""
        print(f"Owner:    {self.name}")
        print(f"Owner ID: {self.owner_id}")
        self.view_owner_pets()

    def view_owner_pets(self):
        """Print the name and ID of every pet registered to this owner."""
        if not self.pets:
            print("No pets registered.")
            return
        print(f"Pets owned by {self.name}:")
        for pet in self.pets:
            print(f"  - {pet.name} (Pet ID: {pet.pet_id}, Owner ID: {pet.owner_id})")


class Schedule:
    def __init__(self, schedule_id, date, owner):
        self.schedule_id = schedule_id
        self.date = date
        self.owner = owner
        # Each entry is a (Task, Pet) tuple so we know which pet owns each task.
        self.tasks = []

    def generate_schedule(self):
        """Collect all tasks from every pet owned by this owner into the schedule."""
        self.tasks = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                self.tasks.append((task, pet))
        print(f"Schedule generated for {self.owner.name} with {len(self.tasks)} task(s).")

    def add_task(self):
        """Prompt the user for task details and add the new task to a chosen pet and the schedule."""
        if not self.owner.pets:
            print("This owner has no pets.")
            return

        print("Which pet is this task for?")
        for i, pet in enumerate(self.owner.pets, start=1):
            print(f"  {i}. {pet.name}")
        pet_choice = int(input("Enter number: ")) - 1
        pet = self.owner.pets[pet_choice]

        name = input("Task name: ")
        description = input("Description: ")
        time = input("Time (HH:MM, 24-hour): ")

        print("Frequency (enter day numbers separated by commas, e.g. 1,3,5):")
        for k, v in FREQUENCY_DAYS.items():
            print(f"  {k}. {v}")
        freq_input = input("Enter numbers: ")
        frequency = [int(x.strip()) for x in freq_input.split(",")]

        print("Priority:")
        for k, v in PRIORITY_LABELS.items():
            print(f"  {k}. {v}")
        priority = int(input("Enter number: "))

        task_id = len(pet.tasks) + 1
        new_task = Task(task_id, name, time, priority, frequency, description)

        conflict = self._check_conflict(new_task)
        if conflict:
            conflict_task, conflict_pet, day_names = conflict
            print(f"Error: '{name}' conflicts with '{conflict_task.name}' ({conflict_pet.name}) at {_format_time(time)} on {day_names}. Task not added.")
            return

        pet.tasks.append(new_task)
        if len(pet.tasks) > 1:
            pet.tasks.sort(key=lambda t: t.time)
        self.tasks.append((new_task, pet))
        print(f"Task '{name}' added for {pet.name}.")

    def remove_task(self):
        """Prompt the user to select a task and remove it from both the schedule and its pet."""
        if not self.tasks:
            print("No tasks in schedule.")
            return

        print("Which task do you want to remove?")
        for i, (task, pet) in enumerate(self.tasks, start=1):
            print(f"  {i}. {task.name} ({pet.name})")
        choice = int(input("Enter number: ")) - 1
        task_to_remove, pet = self.tasks[choice]

        pet.tasks = [t for t in pet.tasks if t.task_id != task_to_remove.task_id]
        self.tasks.pop(choice)
        print(f"Task '{task_to_remove.name}' removed.")

    def update_schedule(self):
        """Interactively add, remove, edit, or mark complete a task on the schedule."""
        while True:
            print("1. Add task")
            print("2. Remove task")
            print("3. Edit existing task")
            print("4. Mark task as complete")
            print("5. Mark task as daily")
            choice = input("Choose an option: ")

            if choice == "1":
                self.add_task()
                break
            elif choice == "2":
                self.remove_task()
                break
            elif choice == "3":
                if not self.tasks:
                    print("No tasks to edit.")
                    return

                print("Which task do you want to edit?")
                for i, (task, pet) in enumerate(self.tasks, start=1):
                    print(f"  {i}. {task.name} ({pet.name})")
                task_choice = int(input("Enter number: ")) - 1
                task, _ = self.tasks[task_choice]

                name = input(f"New name (leave blank to keep '{task.name}'): ") or None
                description = input("New description (leave blank to keep current): ") or None
                time = input(f"New time (leave blank to keep '{task.time}'): ") or None

                print("New frequency — enter day numbers separated by commas (leave blank to keep current):")
                for k, v in FREQUENCY_DAYS.items():
                    print(f"  {k}. {v}")
                freq_input = input("Enter numbers or leave blank: ")
                frequency = [int(x.strip()) for x in freq_input.split(",")] if freq_input else None

                print("New priority (leave blank to keep current):")
                for k, v in PRIORITY_LABELS.items():
                    print(f"  {k}. {v}")
                prio_input = input("Enter number or leave blank: ")
                priority = int(prio_input) if prio_input else None

                task.update_task(name=name, time=time, priority=priority,
                                 frequency=frequency, description=description)
                print("Task updated.")
                break
            elif choice == "4":
                if not self.tasks:
                    print("No tasks to mark complete.")
                    return

                print("Which task do you want to mark as complete?")
                for i, (task, pet) in enumerate(self.tasks, start=1):
                    print(f"  {i}. {task.name} ({pet.name}) — Complete: {task.is_complete}")
                task_choice = int(input("Enter number: ")) - 1
                task, _ = self.tasks[task_choice]
                task.mark_complete()
                print(f"'{task.name}' marked as complete.")
                break
            elif choice == "5":
                if not self.tasks:
                    print("No tasks to mark as daily.")
                    return

                print("Which task do you want to mark as daily?")
                for i, (task, pet) in enumerate(self.tasks, start=1):
                    print(f"  {i}. {task.name} ({pet.name}) — Daily: {task.is_daily}")
                task_choice = int(input("Enter number: ")) - 1
                task, _ = self.tasks[task_choice]
                task.mark_daily()
                print(f"'{task.name}' marked as daily.")
                break
            else:
                print("Invalid option. Please try again.")

    def _task_days(self, task):
        """Return the set of day numbers a task is active on, expanding daily tasks to all 7 days."""
        return ALL_DAYS if task.is_daily else set(task.frequency)

    def _check_conflict(self, new_task):
        """Return (conflicting_task, conflicting_pet, day_names) if new_task clashes with an existing task, else None."""
        new_days = self._task_days(new_task)
        for task, pet in self.tasks:
            overlap = new_days & self._task_days(task) if task.time == new_task.time else set()
            if overlap:
                day_names = ", ".join(FREQUENCY_DAYS[d] for d in sorted(overlap))
                return task, pet, day_names
        return None

    def display_time(self, time_str):
        """Return a 12-hour AM/PM formatted string for the given 24-hour HH:MM input."""
        return _format_time(time_str)

    def _print_task_list(self, task_list, filter_day=None):
        """Print a task list grouped and sorted by day then time; filter_day restricts output to one day."""
        if not task_list:
            print("No tasks to display.")
            return
        # When filter_day is set, only stamp the task under that day.
        # Otherwise expand to all days so multi-day tasks appear under each one.
        expanded = []
        for task, pet in task_list:
            if filter_day is not None:
                days = [filter_day]
            elif task.is_daily:
                days = list(FREQUENCY_DAYS.keys())
            else:
                days = task.frequency
            for day in days:
                expanded.append((day, task.time, task, pet))
        expanded.sort(key=lambda item: (item[0], item[1]))

        current_day = None
        for day, _, task, pet in expanded:
            day_label = FREQUENCY_DAYS.get(day, str(day))
            if day_label != current_day:
                print(f"\n--- {day_label} ---")
                current_day = day_label
            priority_label = PRIORITY_LABELS.get(task.priority, str(task.priority))
            print(f"  [{self.display_time(task.time)}] {task.name} — {pet.name} (Priority: {priority_label})")

    def filter_view(self):
        """Prompt the user to choose a filter (priority, name, time, or day) and display matching tasks."""
        while True:
            print("Filter by:")
            print("  1. Priority")
            print("  2. Task Name")
            print("  3. Time")
            print("  4. Day of week")
            print("  5. Pet name")
            print("  6. Completion status")
            choice = input("Choose an option: ")

            if choice == "1":
                print("Select priority:")
                for k, v in PRIORITY_LABELS.items():
                    print(f"  {k}. {v}")
                priority = int(input("Enter number: "))
                filtered = [(t, p) for t, p in self.tasks if t.priority == priority]
                break
            elif choice == "2":
                keyword = input("Enter name to search: ").strip().lower()
                filtered = [(t, p) for t, p in self.tasks if keyword in t.name.lower()]
                break
            elif choice == "3":
                time_input = input("Enter time (HH:MM): ")
                filtered = [(t, p) for t, p in self.tasks if t.time == time_input]
                break
            elif choice == "4":
                print("Select day:")
                for k, v in FREQUENCY_DAYS.items():
                    print(f"  {k}. {v}")
                day = int(input("Enter number: "))
                filtered = [(t, p) for t, p in self.tasks if day in t.frequency]
                self._print_task_list(filtered, filter_day=day)
                return
            elif choice == "5":
                keyword = input("Enter pet name to search: ").strip().lower()
                filtered = [(t, p) for t, p in self.tasks if keyword in p.name.lower()]
                break
            elif choice == "6":
                print("Select completion status:")
                print("  1. Completed")
                print("  2. Incomplete")
                status_choice = input("Enter number: ")
                if status_choice == "1":
                    filtered = [(t, p) for t, p in self.tasks if t.is_complete]
                elif status_choice == "2":
                    filtered = [(t, p) for t, p in self.tasks if not t.is_complete]
                else:
                    print("Invalid option. Please try again.")
                    continue
                break
            else:
                print("Invalid option. Please try again.")

        self._print_task_list(filtered)

    def view_schedule(self):
        """Display the full schedule or a filtered view, ordered by day of week then time."""
        if not self.tasks:
            print("Schedule is empty. Run generate_schedule() first.")
            return
        while True:
            print("1. Full schedule")
            print("2. Filtered view")
            choice = input("Choose an option: ")

            if choice == "1":
                print(f"\nSchedule for {self.owner.name}:")
                self._print_task_list(self.tasks)
                break
            elif choice == "2":
                self.filter_view()
                break
            else:
                print("Invalid option. Please try again.")




