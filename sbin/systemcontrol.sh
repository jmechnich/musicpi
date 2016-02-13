#!/bin/sh

log="logger -t `basename $0`"
beep="play -q -n synth 0.1 sin 1760"
doublebeep="play -q -n synth 0.1 sine 1760 pad 0 0.2 repeat 1"
port=6789

while true; do
    ans=`nc -l $port`
    case "$ans" in
        mpd_dynamic)
            if ! pgrep mpd_dynamic >/dev/null; then
                $log "Starting mpd_dynamic"
                sudo -u mechnich mpd_dynamic >/dev/null &
                $beep
            else
                $log "Killing mpd_dynamic"
                killall mpd_dynamic
                $doublebeep
            fi
            ;;
        reboot)
            $log "Rebooting"
            $beep
            shutdown -r now
            ;;
        shutdown)
            $log "Shutting down"
            $doublebeep
            killall -9 gmediarender
            shutdown -h now
            ;;
        beep)
            $beep
            ;;
        doublebeep)
            $doublebeep
            ;;
        *)
            $log "Unknown command '$ans'"
            ;;
    esac
done
