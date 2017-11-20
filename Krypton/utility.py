englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
plain_t = lambda cipher_t,k:chr(((ord(cipher_t) - ord('A') - k) % 26) + ord('A'))

def read_file(filename):
	return open(filename, 'r').read().strip('\n').replace(' ','')

def get_single_key(strings):
	return max([(sum([englishLetterFreq[plain_t(s,k)] for s in strings]), k) \
		         for k in range(26)],\
		         key = lambda x: x[0])[1];
def decrypt(ciphertext, key):
	return ''.join([plain_t(ciphertext[i], key[i%len(key)]) for i in range(len(ciphertext))])