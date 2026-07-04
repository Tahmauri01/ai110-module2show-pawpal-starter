# PawPal+ Project Reflection

## 1. System Design

Core actions:
1. Add pet
2. Schedule feeding time
3. Order todays tasks

Main Objects:

Task(class):
Attributes - taskId, name, time, priority, isComplete
Methods - markComplete(), updateDuration(), updatePriority(), viewTaskDetails(), updateTask()

Pet(class):
Attributes - petId, name, owner, age, breed
Methods -  updatePet(), viewPetDetails(), viewPetTasks()

Owner(class):
Attributes - ownerId, name, pets
Methods - updateOwner(), viewOwnerDetails(), viewOwnerPets()

Schedule(class):
Attributes - schkdultId, date, task, owner, pet
Methods - generateSchedule(), updateSchedule(), viewSchedule(), addTask(), removeTask()

**a. Initial design**

- Briefly describe your initial UML design.

My initial design contains four classes: Schedule, Owner, Pet, and Task. Schedule is 1-to-1 with Owner and Pet sincea schedule shouldn't have multiple owners and pets. Owner is 1-to-0 with Pet since an owner can have multiple pets while a pet has one owner. Pet is 1-to-0 with Task since a pet can have multple tasks while a task should be assigned to one pet. Schedule is 1-to-0 with task since the schedule can have multple tasks while the task should only be assigned to one schedule.

- What classes did you include, and what responsibilities did you assign to each?

Schedule contains the date of when the tasks are to be completed. Owner is tied to each of their pets and is responsible for making the tasks and schedule. Pet is what is assigned to the tasks. Tasks belong to the pets and are displayed by the schedule.

**b. Design changes**

- Did your design change during implementation?

Yes

- If yes, describe at least one change and why you made it.

The Pet class was not linked to the Tasks class so a list had to be created for Pet which was stored into Pet.tasks. This change was made because the Task class was linked to the Pet class so the Pet class needed a way to see it's tasks. It was a list since Pet is 1-to-0 to Task.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

Time, priority, name of pet, name of task, day of the week

- How did you decide which constraints mattered most?

Day and time mattered the most since that is what the tasks are ordered by in that order.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

My scheduler only has specific times instead of having the entire duration of the task.

- Why is that tradeoff reasonable for this scenario?

This is reasonable as it could be implemented later since the program is able to run without it.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
