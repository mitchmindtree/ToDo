ToDo CLI
========

My little ToDo CLI, currently in the middle of Dev.


Aims
----

- Simplicity
- Tmux friendly
- Vim integration
- Syncing capabilities with Wunderlist (when official API comes out)
- Recursive sub-listing


Features
--------

    add/+ ""

- adds "" as a task

    add/+ "" +a +b

- adds "" as a task with a and b as tags

    add/+ "" -4

- adds "" to pos 4 for current list

    ls +a

- lists all tasks with "a" tag

    ls

- lists all tasks

    ls +

- lists all tags

    mv 4 1

- moves task in position 4 to position 1 in current list


Structure
---------

    todo = [
        {
          item : ""
          id : 1
          tags : []
        }
        {
          item : ""
          id : 2
          tags : []
        }
        {
          item : ""
          id : 3
          tags : []
        }
    ]
