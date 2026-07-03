import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Owner

def test_mark_complete_changes_status():
    task = Task(task_id=1, name="Walk", time="08:00", priority=2,
                frequency=[1], description="Morning walk")
    assert task.is_complete == False
    task.mark_complete()
    assert task.is_complete == True

def test_add_task_increases_pet_task_count():
    owner = Owner(owner_id=1, name="Alex")
    pet = owner.add_pet(name="Buddy", age=3, breed="Labrador")
    assert len(pet.tasks) == 0
    pet.tasks.append(Task(task_id=1, name="Walk", time="08:00", priority=2,
                          frequency=[1], description="Morning walk"))
    assert len(pet.tasks) == 1
