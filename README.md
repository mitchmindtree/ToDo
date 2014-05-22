ToDo CLI
========

My little ToDo CLI, currently in the middle of Dev.


Aims
----

- Simplicity
- Tmux friendly
- Vim integration
- Syncing capailities with Wunderlist (when official API comes out)
- Recursive sub-listing


Recursive List Structure
------------------------

    todo = [
        {
          item : ""
          id : 1
          todo = [
              {
                item : ""
                id : 0
                todo = []
              }
          ]
        }
        {
          item : ""
          id : 2
          todo = []
        }
        {
          item : ""
          id : 3
          todo = []
        }
    ]
