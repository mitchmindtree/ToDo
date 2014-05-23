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

    add A new dandy task.
    + another new dandy task
    AdD   a nice new task. (works too)

Remove Tasks with `remove` or `rm`

    remove 3
    rm That disgusting task.
    Remove first
    rm last

Move Tasks up and down the list with `move` or `mv`

    move 5 2
    mv 0 last
    mv 7 first

Swap Tasks with `swap` or `sw`

    swap first last
    sw 4 5

Open a task with `open` or `o`

    open 4
    o 1

Close the current task and open its parent with `close` or `cl`

Quit the program with `q`, `x`, `quit` or `exit`


To-Do
-----

- Find tasks containing string and display as child list.
- Add textbox scrolling.
- Redraw upon resizing terminal pane.
- Vim plugin


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
