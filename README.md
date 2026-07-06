# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Schedule for Alex Rivera:

--- Monday ---
  [7:30 AM] Morning Walk — Buddy (Priority: High)
  [6:00 PM] Evening Feeding — Buddy (Priority: Medium)

--- Tuesday ---
  [6:00 PM] Evening Feeding — Buddy (Priority: Medium)

--- Wednesday ---
  [7:30 AM] Morning Walk — Buddy (Priority: High)
  [6:00 PM] Evening Feeding — Buddy (Priority: Medium)

--- Thursday ---
  [6:00 PM] Evening Feeding — Buddy (Priority: Medium)

--- Friday ---
  [7:30 AM] Morning Walk — Buddy (Priority: High)
  [6:00 PM] Evening Feeding — Buddy (Priority: Medium)

--- Saturday ---
  [10:00 AM] Grooming — Luna (Priority: Low)
  [6:00 PM] Evening Feeding — Buddy (Priority: Medium)

--- Sunday ---
  [10:00 AM] Grooming — Luna (Priority: Low)

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
================================= test session starts =============================
platform win32 -- Python 3.11.4, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\tmbo7\OneDrive\Desktop\ai110-module2show-pawpal-starter
collected 2 items                                                                                                                                                                                                                            

tests\test_pawpal.py ..                                                 [100%]

================================= 2 passed in 0.03s ==============================
```

================================== test session starts ===================================
platform win32 -- Python 3.11.4, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\tmbo7\OneDrive\Desktop\ai110-module2show-pawpal-starter
collected 23 items                                                                                                                                                                                                                           

tests\test_pawpal.py .......................                                          [100%]

================================== 23 passed in 0.05s =================================

Tests include checking if these work:
- Time format
- Mark complete twice
- Conflict detection
- Days of week correctness
- Duplicate IDs after deleting then adding Pet
- Sorting by day and time
- Filtering by different attributes
- Schedule generation and regeneration

Confidence Level - 4/5 Stars



## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature           | Method(s)           | Notes |
|-------------------|---------------------|-------|
| Task sorting      | Compsite Sort       | To sort by the day, a list is used to contain the day, time, task, and pet in a tuple. The sort compares the days(first element [0]) in the tuple and will only look at the time(second element[1]) if the days are equal.|
| Filtering         | Linear Search       | To create a filtered list, the list containing all the values is looped through. Whichever value matches the value inputted is appended into the filtered list which is then printed. |
| Conflict handling | Collision Detection | Checks to see if the two times match and gives an error message on the first conflict found |
| Recurring tasks   | Boolean             | Sets attribute is_daily to True. If an object has it set to true then it will be repeated throughout the week on everyday |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Create an owner and a pet with it's age and breed
2. Create a task for your pet including the name, time, day, description, and priority
3. Add as much pets as you need and switch between them to add their tasks
4. Generate a schedule based on all of your pet's tasks, sorted by day then time, including conflict warnings for overalapping tasks
5. Filter your schedule by day, time, name, pet name, priority, or completion
6. Update your schedule by removing/adding tasks, editing a task, marking a task as daily, or marking a task as complete

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
