class Task:
    def __init__(self, task_id, name, time, priority, is_complete):
        self.task_id = task_id
        self.name = name
        self.time = time
        self.priority = priority
        self.is_complete = is_complete

    def mark_complete(self):
        pass

    def view_task_details(self):
        pass

    def update_task(self):
        pass


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
