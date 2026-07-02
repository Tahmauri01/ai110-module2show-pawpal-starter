PRIORITY_LABELS = {1: "Low", 2: "Medium", 3: "High"}
FREQUENCY_DAYS = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}

class Task:
    def __init__(self, task_id, name, time, priority, frequency, description, is_complete=False):
        self.task_id = task_id
        self.name = name
        self.time = time
        self.priority = priority
        self.frequency = frequency
        self.description = description
        self.is_complete = is_complete

    def mark_complete(self):
        self.is_complete = True

    def view_task_details(self):
        hour, minute = map(int, self.time.split(":"))
        period = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12
        formatted_time = f"{display_hour}:{minute:02d} {period}"

        priority_label = PRIORITY_LABELS.get(self.priority, str(self.priority))

        frequency_label = FREQUENCY_DAYS.get(self.frequency, str(self.frequency))

        print(f"Task:        {self.name}")
        print(f"Description: {self.description}")
        print(f"Time:        {formatted_time}")
        print(f"Frequency:   {frequency_label}")
        print(f"Priority:    {priority_label}")
        print(f"Complete:    {self.is_complete}")

    def update_task(self, name=None, time=None, priority=None, frequency=None, description=None):
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
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if breed is not None:
            self.breed = breed

    def view_pet_details(self, owner):
        print(f"Name:  {self.name}")
        print(f"Age:   {self.age}")
        print(f"Breed: {self.breed}")
        print(f"Owner: {owner.name} (ID: {self.owner_id})")

    def view_pet_tasks(self):
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
        pet_id = len(self.pets) + 1
        new_pet = Pet(pet_id, name, self.owner_id, age, breed)
        self.pets.append(new_pet)
        return new_pet

    def remove_pet(self, pet_id):
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def update_owner(self, name=None, add_pet=None, remove_pet_id=None):
        if name is not None:
            self.name = name
        if add_pet is not None:
            self.add_pet(add_pet["name"], add_pet["age"], add_pet["breed"])
        if remove_pet_id is not None:
            self.remove_pet(remove_pet_id)

    def view_owner_details(self):
        print(f"Owner:    {self.name}")
        print(f"Owner ID: {self.owner_id}")
        self.view_owner_pets()

    def view_owner_pets(self):
        if not self.pets:
            print("No pets registered.")
            return
        print(f"Pets owned by {self.name}:")
        for pet in self.pets:
            print(f"  - {pet.name} (Pet ID: {pet.pet_id}, Owner ID: {pet.owner_id})")


class Schedule:
    def __init__(self, schedule_id, date, owner, pet):
        self.schedule_id = schedule_id
        self.date = date
        self.owner = owner
        self.pet = pet
        self.tasks = pet.tasks

    def generate_schedule(self):
        pass

    def update_schedule(self):
        pass

    def view_schedule(self):
        pass

    def add_task(self):
        pass

    def remove_task(self):
        pass
