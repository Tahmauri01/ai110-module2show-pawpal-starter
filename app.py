import streamlit as st
from pawpal_system import Owner, Task, Schedule, PRIORITY_LABELS, FREQUENCY_DAYS

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

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
        st.session_state.owner = new_owner
        st.session_state.schedule = Schedule(
            schedule_id=1, date="2026-07-03", owner=new_owner
        )
        st.rerun()
    else:
        st.stop()

owner = st.session_state.owner
schedule = st.session_state.schedule
pet = owner.pets[0]
#TODO: be able to add more pets and switch through them

st.success(f"Owner: **{owner.name}** — Pet: **{pet.name}** ({pet.breed}, age {pet.age})")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

PRIORITY_MAP = {"Low": 1, "Medium": 2, "High": 3}
DAY_REVERSE = {v: k for k, v in FREQUENCY_DAYS.items()}

col1, col2, col3 = st.columns(3)
with col1:
    task_name = st.text_input("Task name", value="Morning walk")
    task_time = st.text_input("Time (HH:MM, 24-hour)", value="08:00")
with col2:
    task_description = st.text_input("Description", value="")
    priority_str = st.selectbox("Priority", ["Low", "Medium", "High"], index=2)
with col3:
    selected_days = st.multiselect("Frequency", list(FREQUENCY_DAYS.values()))

if st.button("Add task"):
    frequency = [DAY_REVERSE[d] for d in selected_days]
    task_id = len(pet.tasks) + 1
    new_task = Task(
        task_id=task_id,
        name=task_name,
        time=task_time,
        priority=PRIORITY_MAP[priority_str],
        frequency=frequency,
        description=task_description,
    )
    pet.tasks.append(new_task)
    schedule.tasks.append((new_task, pet))
    st.success(f"Task '{task_name}' added for {pet.name}.")

if schedule.tasks:
    st.write("Current tasks:")
    rows = []
    for task, p in schedule.tasks:
        freq_label = ", ".join(FREQUENCY_DAYS[d] for d in task.frequency) if task.frequency else "—"
        rows.append({
            "Task": task.name,
            "Pet": p.name,
            "Time": task.time,
            "Priority": PRIORITY_LABELS[task.priority],
            "Frequency": freq_label,
            "Complete": task.is_complete,
        })
    st.table(rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
