englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
plain_t = lambda cipher_t,k:chr(((ord(cipher_t) - ord('A') - k) % 26) + ord('A'))

def read_file(filename):
	return open(filename, 'r').read().strip('\n').replace(' ','')

def get_key():
	f1 = read_file("found1")
	f2 = read_file("found2")

	strs = [[f1[j] for j in range(len(f1)) if j % 6 == i]\
	         + [f2[j] for j in range(len(f2)) if j % 6 == i] for i in range(6)]
	key = [max([(sum([englishLetterFreq[plain_t(j,k)] for j in strs[i]]), k) \
		         for k in range(26)],\
		         key = lambda x: x[0])[1] \
	       for i in range(6)]
	return key

def decrypt():
	key = get_key()
	plaintext = ""
	k5 = read_file("krypton5")
	for i in range(len(k5)):
		plaintext += plain_t(k5[i], key[i%6])
	return plaintext
print(decrypt())


