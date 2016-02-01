#!/bin/sh

log="logger -t `basename $0`"
PORT=6789

while true; do
    ANS=`nc -l $PORT`
    case "$ANS" in
        mpd_dynamic)
            if ! pgrep mpd_dynamic >/dev/null; then
                $log "Starting mpd_dynamic"
                sudo -u mechnich mpd_dynamic >/dev/null &
            else
                $log "Not starting mpd_dynamic: already running"
            fi
            ;;
        reboot)
            $log "Rebooting"
            shutdown -r now
            ;;
        shutdown)
            $log "Shutting down"
            shutdown -h now
            ;;
        *)
            $log "Unknown command '$ANS'"
            ;;
    esac
done
