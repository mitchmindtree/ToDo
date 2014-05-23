ToDo CLI
========

My little ToDo CLI, currently in the middle of Dev.


Aims
----

- Tmux friendly
- Vim integration
- Syncing capailities with Wunderlist (when official API comes out)
- Simplicity
- Recursive sub-listing


Usage
-----

See the list of commands with `h`, `help` or `?`

Add Tasks with `add` or `+`

    add A new dandy task.               # Adds "A new dandy task." as a task.
    + another new dandy task            # Adds "another new dandy task"
    AdD   a nice new task.              # Adds "a nice new task."

Remove Tasks with `remove` or `rm`

    remove 3                    # Removes 3rd task in list.
    rm That disgusting task.    # Removes "That disgusting task."
    Remove first                # Removes the first task in list.
    rm last                     # Removes the last task in list.

Move Tasks up and down the list with `move` or `mv`

    move 5 2    # Moves 5th task to 2nd position and shuffles list back.
    mv 0 last   # Moves first task to the end of the list.
    mv 7 first  # Moves 7th task to the front of the list.

Swap Tasks with `swap` or `sw`

    swap first last     # Swaps the first and last tasks.
    sw 4 5              # Swaps the fourth and fifth tasks.

Open a task with `open` or `o`

    open 4  # Opens the 4th task as the main task.
    o 1     # Opens the 1st task as the main task.

Close the current task and open its parent with `close` or `cl`

Quit the program with `q`, `x`, `quit` or `exit`


To-Do
-----

- Find tasks containing string and display as child list.
- Add textbox scrolling.
- Redraw upon resizing terminal pane.
- Vim plugin
- Switch cursor between list and command line.
- Add `cross` / `cr` to cross off tasks and move them to bottom (removes ID from draw)
- Fix remove crash
- Finish help command


Recursive List Structure
------------------------

    Tasks = [
        {
          Task : ""
          id : 1
          Tasks = [
              {
                Task : ""
                id : 0
                Tasks = [etc...]
              }
          ]
        }
        {
          Task : ""
          id : 2
          Tasks = []
        }
        {
          Task : ""
          id : 3
          Tasks = []
        }
    ]
