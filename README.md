# GDB configuration

This is my configuration for use with [GDB Dashboard](https://github.com/cyrus-and/gdb-dashboard), which I use as my main `.gdbinit` in my home directory. You should check out the docs there too.

## Setup

### tmux

Does not require but is really nice with tmux. If you want mouse scrolling in the debugger, you can add `setw -g mouse on` to your `.tmux.conf` (for `tmux` < 2.1, use `setw -g mode-mouse on` instead). tmux can make the screen two side-by-side panes if you invoke GDB with the `gdb-tmux.sh` script. The `gdb-tmux-vertical.sh` script runs the debugger with a vertical split instead. I suggest symlinking it under somewhere in your path. I also added `alias gdbh="gdb-tmux"` and `alias gdbv="gdb-tmux-vertical"` to my `.bashrc` in my home directory.

**Note:** The tmux scripts have some limitations; namely they only work as intended if you invoke GDB with no arguments or with a binary as its sole argument. I also do not recommend aliasing `gdb` to either of the scripts because the scripts themselves call GDB.

### GDB

Requires a build that uses Python 3; check via `ldd $(which gdb) | grep python`. I'm using 3.10.

### Configuration

`.gdbinit.d/` belongs in the home directory and is loaded in addition to `.gdbinit`. Suggest it also be symlinked inside the home directory. It contains:

 - Another config file called simply `init`, which sources every script in the `.gdbinit.d/gdb/` subdirectory and can have other options that might belong in a `.gdbinit` file but that you would like to separate from the Dashborad `.gdbinit`.
 - A subdirectory called `python` which contains any Python scripts you want to be able to use inside of GDB (see [the documentation](https://sourceware.org/gdb/onlinedocs/gdb/Python.html#Python)).
 - A subdirectory called `gdb` which contains any GDB command scripts (see [the documentation](https://sourceware.org/gdb/onlinedocs/gdb/Sequences.html#Sequences)).

## Further reading

- [All GDB docs](https://sourceware.org/gdb/onlinedocs/gdb/)
- [Red Hat blog article on the GDB Python API](https://developers.redhat.com/blog/2017/11/10/gdb-python-api)

