#!/bin/bash

function set_title ( )
{
    case $TERM in
        *term | xterm-color | rxvt | vt100 | gnome* )
            echo -n -e "\033]0;$*\007" ;;
        *)  ;;
    esac
}

function remove_process() {
    for _program in java Terminal firefox celery rabbitmq;
    do
        pid=`ps -ef|grep -v "grep" |grep $_program |awk ' { print $2 }'`
        if [[ -n $pid ]]; then
            echo "Killing $_program PID=$pid"
            kill -TERM $pid
            kill -9 $pid
            echo -e ".\c"
        fi
    done
}
remove_process

function run_java() {
    osascript \
        -e "tell application \"Terminal\"" \
        -e "do script \"cd\" in front window" \
        -e "do script \"java -jar selenium-server-standalone-2.45.0.jar\" in front window" \
        -e "end tell" > /dev/null
}
#run_java

function new_tab() {
  osascript 2>/dev/null <<EOF
    tell application "Terminal"
        activate
        do script with command "cd \"$PWD\"; $*" in window 1
        set number of rows of first window to 34
        set number of columns of first window to 96
        set custom title of first window to "Java to celery"
    end tell
EOF
}
#        -e "tell application \"System Events\" to keystroke \"t\" using {command down}" \
#new_tab

function run_rootair() {
    osascript \
        -e "tell application \"Terminal\"" \
        -e "do script \"cd ~/Downloads/balance-pack/balance\" in front window" \
        -e "do script \". ../bin/activate\" in front window" \
        -e "do script \"python manage.py runserver\" in front window" \
        -e "end tell" > /dev/null
}
#run_rootair

sudo rabbitmq-server -detached
. ../bin/activate
celery -A tasks worker --loglevel=info
