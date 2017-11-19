englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

def read_file(filename):
	return open(filename, 'r').read().strip('\n').replace(' ','')

f1 = read_file("found1")
f2 = read_file("found2")

strs = [[f1[j] for j in range(len(f1)) if j % 6 == i]\
         + [f2[j] for j in range(len(f2)) if j % 6 == i] for i in range(6)]

key = []
for i in range(6):
	s = strs[i]
	max_s = 0
	best_k = -1
	for k in range(26): 
		score = 0
		for j in s:
			c = chr(((ord(j) - ord('A') - k) % 26) + ord('A'))
			score += englishLetterFreq[c]
		if score > max_s:
			max_s = score
			best_k = k
	key.append(best_k)
print(key)

def decrypt():
	plaintext = ""
	k5 = read_file("krypton5")
	for i in range(len(k5)):
		plaintext += chr(((ord(k5[i])-ord('A') - key[i%6]) % 26) + ord('A'))
	return plaintext
print(decrypt())


