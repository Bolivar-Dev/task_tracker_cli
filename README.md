Task Tracker CLI (Command Line Interface)

Task Tracker CLI is a feature that allows us to add, update, mark, and also delete task in JSON file with a simple command line application in it. It also let us view a list of task based on their status.
Features

    Add: Add a new task with a description and a default status of "todo",
    List: View tasks based on their status (todo, in progress, done, or all).
    Update: Update the description of an existing task based on their ID.
    Mark: Change the status of a task into "in progress" or "done" based on their ID.
    Delete: Remove an existing task based on their ID.

Usage
1) Add Task

To add a new task, use the next command structure:
add "task description"

2) List Tasks

To list tasks based on their status type list. it will show you a menu with options, select you option desired.
- list

3) Update Task Description

To update the status of the taks type mark followed by id, example:
- mark id

4) Delete Task

To delete a task type delete followed by id of the task:
- delete 2
