PRIORITY_LABELS = {1: "Low", 2: "Medium", 3: "High"}

class Task:
    def __init__(self, task_id, name, time, priority, is_complete=False):
        self.task_id = task_id
        self.name = name
        self.time = time
        self.priority = priority
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

        print(f"Task:     {self.name}")
        print(f"Time:     {formatted_time}")
        print(f"Priority: {priority_label}")
        print(f"Complete: {self.is_complete}")

    def update_task(self, name=None, time=None, priority=None):
        if name is not None:
            self.name = name
        if time is not None:
            self.time = time
        if priority is not None:
            self.priority = priority


class Pet:
    def __init__(self, pet_id, name, owner_id, age, breed):
        self.pet_id = pet_id
        self.name = name
        self.owner_id = owner_id
        self.age = age
        self.breed = breed
        self.tasks = []

    def update_pet(self):
        pass

    def view_pet_details(self):
        pass

    def view_pet_tasks(self):
        pass


class Owner:
    def __init__(self, owner_id, name):
        self.owner_id = owner_id
        self.name = name
        self.pets = []

    def update_owner(self):
        pass

    def view_owner_details(self):
        pass

    def view_owner_pets(self):
        pass


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
