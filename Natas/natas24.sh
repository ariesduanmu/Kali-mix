natas24_(){
	user_pass="natas24:OsRmXFguozKpTZZ5X14zNO43379LZveg"
	url="http://natas24.natas.labs.overthewire.org"

	val=$(curl -isu $user_pass $url?passwd=OsRmXFguozKpTZZ5X14zNO43379LZveg)
	echo "$val"
}

