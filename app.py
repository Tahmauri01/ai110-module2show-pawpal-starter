import streamlit as st
from pawpal_system import Owner, Task, Schedule, PRIORITY_LABELS, FREQUENCY_DAYS, _format_time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

PRIORITY_MAP = {"Low": 1, "Medium": 2, "High": 3}
DAY_REVERSE  = {v: k for k, v in FREQUENCY_DAYS.items()}

# ── Owner & Pet Setup ────────────────────────────────────────────────────────
st.subheader("Owner & Pet Setup")

if "owner" not in st.session_state:
    with st.form("setup_form"):
        st.markdown("**Owner**")
        input_owner_name = st.text_input("Owner name", value="Jordan")
        st.markdown("**Pet**")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            input_pet_name = st.text_input("Pet name", value="Mochi")
        with col_b:
            input_pet_age = st.number_input("Age", min_value=0, max_value=30, value=2)
        with col_c:
            input_pet_breed = st.text_input("Breed", value="Golden Retriever")
        submitted = st.form_submit_button("Create Owner & Pet")

    if submitted:
        new_owner = Owner(owner_id=1, name=input_owner_name)
        new_owner.add_pet(name=input_pet_name, age=int(input_pet_age), breed=input_pet_breed)
        st.session_state.owner    = new_owner
        st.session_state.schedule = Schedule(schedule_id=1, date="2026-07-05", owner=new_owner)
        st.rerun()
    else:
        st.stop()

owner    = st.session_state.owner
schedule = st.session_state.schedule
pet      = owner.pets[0]

st.success(f"Owner: **{owner.name}** — Pet: **{pet.name}** ({pet.breed}, age {pet.age})")

with st.expander("Add another pet"):
    with st.form("add_pet_form"):
        np_col1, np_col2, np_col3 = st.columns(3)
        with np_col1:
            new_pet_name = st.text_input("Pet name")
        with np_col2:
            new_pet_age = st.number_input("Age", min_value=0, max_value=30, value=1)
        with np_col3:
            new_pet_breed = st.text_input("Breed")
        pet_submitted = st.form_submit_button("Add Pet")
    if pet_submitted and new_pet_name.strip():
        owner.add_pet(name=new_pet_name.strip(), age=int(new_pet_age), breed=new_pet_breed.strip())
        st.success(f"Pet **'{new_pet_name}'** added.")
        st.rerun()

st.divider()

# ── Add Task ─────────────────────────────────────────────────────────────────
st.subheader("Add Task")

with st.form("add_task_form"):
    pet_names      = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Pet", pet_names)
    col1, col2, col3 = st.columns(3)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk")
        task_time = st.text_input("Time (HH:MM, 24-hour)", value="08:00")
    with col2:
        task_desc     = st.text_input("Description", value="")
        priority_str  = st.selectbox("Priority", ["Low", "Medium", "High"], index=2)
    with col3:
        selected_days = st.multiselect("Frequency", list(FREQUENCY_DAYS.values()))
        is_daily      = st.checkbox("Daily (every day)")
    add_submitted = st.form_submit_button("Add Task")

if add_submitted:
    task_pet  = next(p for p in owner.pets if p.name == selected_pet_name)
    frequency = list(FREQUENCY_DAYS.keys()) if is_daily else [DAY_REVERSE[d] for d in selected_days]
    task_id   = len(task_pet.tasks) + 1
    new_task  = Task(
        task_id=task_id,
        name=task_name,
        time=task_time,
        priority=PRIORITY_MAP[priority_str],
        frequency=frequency,
        description=task_desc,
        is_daily=is_daily,
    )
    conflict = schedule._check_conflict(new_task)
    if conflict:
        conflict_task, conflict_pet, day_names = conflict
        st.error(
            f"Conflict: **'{task_name}'** clashes with **'{conflict_task.name}'** "
            f"({conflict_pet.name}) at {_format_time(task_time)} on {day_names}."
        )
    else:
        task_pet.tasks.append(new_task)
        if len(task_pet.tasks) > 1:
            task_pet.tasks.sort(key=lambda t: t.time)
        schedule.tasks.append((new_task, task_pet))
        st.success(f"Task **'{task_name}'** added for {task_pet.name}.")

st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.subheader("Schedule")

if st.button("Generate / Refresh Schedule"):
    schedule.generate_schedule()
    st.success(f"Schedule generated with {len(schedule.tasks)} task(s).")

# Helper: build display rows from a (task, pet) list, respecting filter_day
def build_rows(task_list, filter_day=None):
    expanded = []
    for task, p in task_list:
        if filter_day is not None:
            days = [filter_day]
        elif task.is_daily:
            days = list(FREQUENCY_DAYS.keys())
        else:
            days = task.frequency
        for day in days:
            expanded.append((day, task.time, task, p))
    expanded.sort(key=lambda item: (item[0], item[1]))
    rows = []
    last_day = None
    for day, _, task, p in expanded:
        day_label = FREQUENCY_DAYS[day]
        rows.append({
            "Day":      day_label if day_label != last_day else "",
            "Time":     _format_time(task.time),
            "Task":     task.name,
            "Pet":      p.name,
            "Priority": PRIORITY_LABELS.get(task.priority, str(task.priority)),
        })
        last_day = day_label
    return rows

if schedule.tasks:

    # ── Filter ────────────────────────────────────────────────────────────────
    st.markdown("#### Filter")
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        filter_by = st.selectbox(
            "Filter by",
            ["None", "Priority", "Task name", "Time", "Day of week", "Pet name", "Completion status"],
        )
    with fcol2:
        filter_value = None
        if filter_by == "Priority":
            filter_value = st.selectbox("Priority value", ["Low", "Medium", "High"])
        elif filter_by == "Task name":
            filter_value = st.text_input("Keyword")
        elif filter_by == "Time":
            filter_value = st.text_input("Time (HH:MM)")
        elif filter_by == "Day of week":
            filter_value = st.selectbox("Day", list(FREQUENCY_DAYS.values()))
        elif filter_by == "Pet name":
            filter_value = st.text_input("Pet name keyword")
        elif filter_by == "Completion status":
            filter_value = st.selectbox("Status", ["Complete", "Incomplete"])

    filter_day = None
    if filter_by == "None" or not filter_value:
        filtered = schedule.tasks
    elif filter_by == "Priority":
        p_val    = PRIORITY_MAP[filter_value]
        filtered = [(t, p) for t, p in schedule.tasks if t.priority == p_val]
    elif filter_by == "Task name":
        kw       = filter_value.strip().lower()
        filtered = [(t, p) for t, p in schedule.tasks if kw in t.name.lower()]
    elif filter_by == "Time":
        filtered = [(t, p) for t, p in schedule.tasks if t.time == filter_value]
    elif filter_by == "Day of week":
        filter_day = DAY_REVERSE[filter_value]
        active_days = lambda t: list(FREQUENCY_DAYS.keys()) if t.is_daily else t.frequency
        filtered = [(t, p) for t, p in schedule.tasks if filter_day in active_days(t)]
    elif filter_by == "Pet name":
        kw       = filter_value.strip().lower()
        filtered = [(t, p) for t, p in schedule.tasks if kw in p.name.lower()]
    elif filter_by == "Completion status":
        want_complete = filter_value == "Complete"
        filtered = [(t, p) for t, p in schedule.tasks if t.is_complete == want_complete]
    else:
        filtered = schedule.tasks

    rows = build_rows(filtered, filter_day=filter_day)
    if rows:
        st.table(rows)
    else:
        st.info("No tasks match the current filter.")

    st.divider()

    # ── Update Schedule ───────────────────────────────────────────────────────
    st.subheader("Update Schedule")

    task_labels  = [
        f"{task.name} — {p.name} ({_format_time(task.time)})"
        for task, p in schedule.tasks
    ]
    update_action  = st.selectbox("Action", ["Remove task", "Edit task", "Mark complete", "Mark daily"])
    selected_label = st.selectbox("Select task", task_labels)
    selected_idx   = task_labels.index(selected_label)
    selected_task, selected_pet = schedule.tasks[selected_idx]

    if update_action == "Remove task":
        if st.button("Remove"):
            selected_pet.tasks = [t for t in selected_pet.tasks if t.task_id != selected_task.task_id]
            schedule.tasks.pop(selected_idx)
            st.success(f"'{selected_task.name}' removed.")
            st.rerun()

    elif update_action == "Edit task":
        with st.form("edit_form"):
            e_name     = st.text_input("Name",        value=selected_task.name)
            e_time     = st.text_input("Time (HH:MM)", value=selected_task.time)
            e_desc     = st.text_input("Description",  value=selected_task.description)
            e_priority = st.selectbox("Priority", ["Low", "Medium", "High"],
                                      index=selected_task.priority - 1)
            e_days     = st.multiselect(
                "Frequency", list(FREQUENCY_DAYS.values()),
                default=[FREQUENCY_DAYS[d] for d in selected_task.frequency
                         if d in FREQUENCY_DAYS],
            )
            edit_submitted = st.form_submit_button("Save changes")
        if edit_submitted:
            selected_task.update_task(
                name=e_name,
                time=e_time,
                priority=PRIORITY_MAP[e_priority],
                frequency=[DAY_REVERSE[d] for d in e_days],
                description=e_desc,
            )
            st.success("Task updated.")
            st.rerun()

    elif update_action == "Mark complete":
        if st.button("Mark as complete"):
            selected_task.mark_complete()
            st.success(f"'{selected_task.name}' marked as complete.")
            st.rerun()

    elif update_action == "Mark daily":
        if st.button("Mark as daily"):
            selected_task.mark_daily()
            st.success(f"'{selected_task.name}' marked as daily.")
            st.rerun()

else:
    st.info("No tasks in schedule yet. Add tasks above, then click **Generate / Refresh Schedule**.")
