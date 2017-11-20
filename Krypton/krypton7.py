cipter_k7 = 'PNUKLYLWRQKGKBE'
plain_t = 'A'*16
ciper_t = 'EICTDGYIYZKTHNSI' #this is key

def en_xor(s1,s2):
	return chr(((ord(s1) + ord(s2) - 2 * ord('A')) % 26) + ord('A'))
def de_xor(c,k):
	return chr(((ord(c) - ord(k)) % 26) + ord('A'))


plain = ''.join([de_xor(cipter_k7[i], ciper_t[i]) for i in range(15)])
print(plain)
