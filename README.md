ToDo
====

A little ToDo CLI/API/APP! Much excite.


![ToDo Pic](https://raw.github.com/mitchmindtree/ToDo-CLI/master/todopic.png)


Features
--------

- Simplicity.
- Add, remove, swap and move tasks.
- Recursive, infinite sub-listing!
- Tmux friendly.
- Resizable.
- Vim integration (todo).
- REST API? (todo).


Usage
-----


Download and run it with:

    $ git clone https://github.com/mitchmindtree/ToDo-CLI.git ~/
    $ cd ~/ToDo-CLI
    $ python ToDo.py


See the list of commands by entering `h`, `help` or `?`


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

Scroll down the list with `ctrl+j`
Scroll up the list with `ctrl+k`

If no command is detected upon entering some text, the text will simply be
added as a task to the current list (like the `add`/`+` command).


To-Do
-----


Both features and fixes can be found [here] (https://github.com/ToDoDev/ToDo/issues).


Maintainers
-----------

[Mitch] (https://github.com/mitchmindtree) and [Aden] (https://github.com/adentranter)
