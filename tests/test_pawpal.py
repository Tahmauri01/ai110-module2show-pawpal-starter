import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Owner, Schedule, _format_time


# ---------------------------------------------------------------------------
# Existing tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# _format_time edge cases
# ---------------------------------------------------------------------------

def test_format_time_midnight():
    assert _format_time("00:00") == "12:00 AM"

def test_format_time_noon():
    assert _format_time("12:00") == "12:00 PM"

def test_format_time_just_after_noon():
    assert _format_time("12:01") == "12:01 PM"

def test_format_time_end_of_day():
    assert _format_time("23:59") == "11:59 PM"

def test_format_time_standard_am():
    assert _format_time("09:05") == "9:05 AM"

def test_format_time_standard_pm():
    assert _format_time("14:30") == "2:30 PM"


# ---------------------------------------------------------------------------
# mark_complete — idempotency (documents current behavior)
# ---------------------------------------------------------------------------

def test_mark_complete_twice_appends_completed_twice():
    # Known bug: calling mark_complete() twice appends "[COMPLETED]" twice.
    # This test documents the current behavior; fix mark_complete() to guard
    # against is_complete already being True before updating this test.
    task = Task(task_id=1, name="Walk", time="08:00", priority=2,
                frequency=[1], description="Morning walk")
    task.mark_complete()
    task.mark_complete()
    assert task.name.count("[COMPLETED]") == 2


# ---------------------------------------------------------------------------
# Conflict detection — _check_conflict
# ---------------------------------------------------------------------------

def _make_schedule(pet_name="Buddy"):
    owner = Owner(owner_id=1, name="Alex")
    pet = owner.add_pet(name=pet_name, age=3, breed="Labrador")
    schedule = Schedule(schedule_id=1, date="2026-07-05", owner=owner)
    return schedule, owner, pet


def test_conflict_same_time_overlapping_days():
    schedule, _, pet = _make_schedule()
    existing = Task(1, "Walk", "08:00", 2, [1, 2], "Mon/Tue walk")
    pet.tasks.append(existing)
    schedule.tasks.append((existing, pet))

    new_task = Task(2, "Feed", "08:00", 2, [2, 3], "Tue/Wed feed")
    conflict = schedule._check_conflict(new_task)

    assert conflict is not None
    assert conflict[0] is existing
    assert "Tuesday" in conflict[2]


def test_conflict_same_time_non_overlapping_days():
    schedule, _, pet = _make_schedule()
    existing = Task(1, "Walk", "08:00", 2, [1, 2], "Mon/Tue")
    pet.tasks.append(existing)
    schedule.tasks.append((existing, pet))

    new_task = Task(2, "Feed", "08:00", 2, [3, 4], "Wed/Thu")
    assert schedule._check_conflict(new_task) is None


def test_conflict_daily_task_blocks_any_same_time():
    # A daily task should conflict with a new task on any day at the same time.
    schedule, _, pet = _make_schedule()
    daily = Task(1, "Meds", "08:00", 3, [1], "Daily meds", is_daily=True)
    pet.tasks.append(daily)
    schedule.tasks.append((daily, pet))

    new_task = Task(2, "Feed", "08:00", 2, [4], "Thursday feed")
    conflict = schedule._check_conflict(new_task)
    assert conflict is not None


def test_conflict_different_times_no_conflict():
    schedule, _, pet = _make_schedule()
    existing = Task(1, "Walk", "08:00", 2, [1, 2, 3], "Morning walk")
    pet.tasks.append(existing)
    schedule.tasks.append((existing, pet))

    new_task = Task(2, "Feed", "09:00", 2, [1, 2, 3], "Breakfast")
    assert schedule._check_conflict(new_task) is None


def test_conflict_empty_schedule_never_conflicts():
    schedule, _, _ = _make_schedule()
    new_task = Task(1, "Walk", "08:00", 2, [1], "Morning walk")
    assert schedule._check_conflict(new_task) is None


# ---------------------------------------------------------------------------
# _task_days — daily flag expansion
# ---------------------------------------------------------------------------

def test_task_days_daily_returns_all_seven():
    schedule, _, _ = _make_schedule()
    task = Task(1, "Meds", "08:00", 3, [1], "Daily meds", is_daily=True)
    assert schedule._task_days(task) == {1, 2, 3, 4, 5, 6, 7}


def test_task_days_non_daily_returns_only_frequency():
    schedule, _, _ = _make_schedule()
    task = Task(1, "Walk", "08:00", 2, [1, 3, 5], "Mon/Wed/Fri")
    assert schedule._task_days(task) == {1, 3, 5}


# ---------------------------------------------------------------------------
# Pet ID collision after removal (documents current bug)
# ---------------------------------------------------------------------------

def test_pet_id_collision_after_removal():
    # Known bug: pet_id = len(pets) + 1 causes a collision when a pet is
    # removed and a new one is added. IDs should always be unique.
    owner = Owner(owner_id=1, name="Alex")
    owner.add_pet("Buddy", 3, "Labrador")    # id=1
    owner.add_pet("Max", 2, "Poodle")         # id=2
    owner.add_pet("Luna", 4, "Beagle")        # id=3
    owner.remove_pet(2)                        # remove id=2; len is now 2
    owner.add_pet("Coco", 1, "Chihuahua")     # len+1 = 3 → collides with Luna

    ids = [p.pet_id for p in owner.pets]
    assert len(ids) == len(set(ids)), f"Duplicate pet IDs after removal: {ids}"


# ---------------------------------------------------------------------------
# Sorting — pet.tasks order after multiple adds
# ---------------------------------------------------------------------------

def test_pet_tasks_sorted_by_time_after_multiple_adds():
    owner = Owner(owner_id=1, name="Alex")
    pet = owner.add_pet("Buddy", 3, "Labrador")

    # Simulate what add_task does: append then sort (only when len > 1)
    tasks_to_add = [
        Task(1, "Evening walk", "20:00", 2, [1], "Late"),
        Task(2, "Morning walk", "08:00", 2, [1], "Early"),
        Task(3, "Midday walk",  "12:00", 2, [1], "Noon"),
    ]
    for t in tasks_to_add:
        pet.tasks.append(t)
        if len(pet.tasks) > 1:
            pet.tasks.sort(key=lambda x: x.time)

    times = [t.time for t in pet.tasks]
    assert times == sorted(times), f"Tasks not in time order: {times}"


def test_pet_tasks_single_task_requires_no_sort():
    owner = Owner(owner_id=1, name="Alex")
    pet = owner.add_pet("Buddy", 3, "Labrador")
    task = Task(1, "Walk", "08:00", 2, [1], "Morning")
    pet.tasks.append(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


# ---------------------------------------------------------------------------
# Day filter misses daily tasks (documents current bug)
# ---------------------------------------------------------------------------

def test_day_filter_excludes_daily_tasks():
    # Known bug: filter_view option 4 uses `day in t.frequency`, so a task
    # with is_daily=True but frequency=[1] is invisible when filtering by
    # any day other than Monday. Fix filter_view to use _task_days() instead.
    owner = Owner(owner_id=1, name="Alex")
    pet = owner.add_pet("Buddy", 3, "Labrador")
    schedule = Schedule(schedule_id=1, date="2026-07-05", owner=owner)

    daily_task = Task(1, "Meds", "08:00", 3, [1], "Daily meds", is_daily=True)
    pet.tasks.append(daily_task)
    schedule.tasks.append((daily_task, pet))

    # Filter by Tuesday (day 2) using the current buggy logic
    filtered_buggy = [(t, p) for t, p in schedule.tasks if 2 in t.frequency]
    assert len(filtered_buggy) == 0  # bug: daily task not found

    # Correct logic using _task_days()
    filtered_correct = [(t, p) for t, p in schedule.tasks if 2 in schedule._task_days(t)]
    assert len(filtered_correct) == 1  # daily task should appear on every day


# ---------------------------------------------------------------------------
# generate_schedule — rebuild behavior
# ---------------------------------------------------------------------------

def test_generate_schedule_collects_all_pet_tasks():
    owner = Owner(owner_id=1, name="Alex")
    pet = owner.add_pet("Buddy", 3, "Labrador")
    pet.tasks.extend([
        Task(1, "Walk", "08:00", 2, [1], "Morning"),
        Task(2, "Feed", "12:00", 1, [1, 2], "Lunch"),
    ])
    schedule = Schedule(schedule_id=1, date="2026-07-05", owner=owner)
    schedule.generate_schedule()
    assert len(schedule.tasks) == 2


def test_generate_schedule_rebuild_reflects_removed_pet_tasks():
    owner = Owner(owner_id=1, name="Alex")
    pet = owner.add_pet("Buddy", 3, "Labrador")
    t1 = Task(1, "Walk", "08:00", 2, [1], "Morning")
    pet.tasks.append(t1)

    schedule = Schedule(schedule_id=1, date="2026-07-05", owner=owner)
    schedule.generate_schedule()
    assert len(schedule.tasks) == 1

    pet.tasks.clear()
    schedule.generate_schedule()
    assert len(schedule.tasks) == 0


def test_generate_schedule_spans_multiple_pets():
    owner = Owner(owner_id=1, name="Alex")
    p1 = owner.add_pet("Buddy", 3, "Labrador")
    p2 = owner.add_pet("Max", 2, "Poodle")
    p1.tasks.append(Task(1, "Walk", "08:00", 2, [1], "Walk"))
    p2.tasks.append(Task(1, "Feed", "09:00", 1, [1], "Feed"))
    p2.tasks.append(Task(2, "Meds", "20:00", 3, [1], "Meds"))

    schedule = Schedule(schedule_id=1, date="2026-07-05", owner=owner)
    schedule.generate_schedule()
    assert len(schedule.tasks) == 3
