#!/usr/bin/bash

# See https://github.com/cyrus-and/gdb-dashboard/wiki/Use-multiple-terminals

split="v"
session="gdb"
output=$(tmux new-session -s "$session"0 'id="$(tmux split-pane -'"$split"'PF "#D" "tail -f /dev/null")"; tmux last-pane; tty="$(tmux display-message -p -t "$id" "#{pane_tty}")"; gdb -ex "dashboard -output $tty" '"$@"'; tmux kill-pane -t "$id";' 2>&1)
search=$(echo $output | sed -n '/duplicate session/p')

if [[ "$search" == "$output" ]]; then
    echo $output
    session_num=$(echo $output | sed "s/^duplicate session: gdb_sess//")
    let next=$session_num+1
    tmux new-session -s "$session$next" 'id="$(tmux split-pane -'"$split"'PF "#D" "tail -f /dev/null")"; tmux last-pane; tty="$(tmux display-message -p -t "$id" "#{pane_tty}")"; gdb -ex "dashboard -output $tty" '"$@"'; tmux kill-pane -t "$id";'
fi

