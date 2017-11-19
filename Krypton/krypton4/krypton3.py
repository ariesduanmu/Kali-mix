
#https://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html
englishLetterFreq = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
most_common_pairs = ['TH', 'EA', 'OF', 'TO', 'IN', 'IT', 'IS', 'BE', 'AS', 'SO', 'WE', 'HE', 'BY', 'OR', 'ON', 'DO', 'IF', 'ME', 'UP']
most_common_repeat = ['SS', 'EE', 'TT', 'FF', 'LL', 'MM', 'OO']
most_common_triplets = ['THE','EST','FOR','AND','HIS','ENT','THA']


def read_file(filename):
	return open(filename, 'r').read().strip('\n').replace(' ','')
strs = read_file("found1")+read_file("found2")+read_file("found3")+read_file("krypton4")


# letter frequence
letter_frequence = [[0, chr(ord('A') + i)] for i in range(26)]
for s in strs:
	if s != " ":
		letter_frequence[ord(s) - ord('A')][0] += 1

letter_frequence = sorted(letter_frequence, key = lambda x: -x[0])

# pais
pairs = {}
repeat_pairs = {}
for i in range(len(strs)-1):
	s = strs[i:i+2]
	if s[0] == s[1]:
		if s in repeat_pairs:
			repeat_pairs[s] += 1
		else:
			repeat_pairs[s] = 1
	else:
		if s in pairs:
			pairs[s] += 1
		else:
			pairs[s] = 1
pairs_frequence = sorted([(k, pairs[k]) for k in pairs], key = lambda x: -x[1])
repeat_pairs_frequence = sorted([(k, repeat_pairs[k]) for k in repeat_pairs], key = lambda x: -x[1])

#triplets
triplets = {}
for i in range(len(strs)-2):
	s = strs[i:i+3]
	if s in triplets:
		triplets[s] += 1
	else:
		triplets[s] = 1
triplets_frequence = sorted([(k, triplets[k]) for k in triplets], key = lambda x: -x[1])

#four
fours = {}
for i in range(len(strs)-3):
	s = strs[i:i+4]
	if s in fours:
		fours[s] += 1
	else:
		fours[s] = 1
fours_frequence = sorted([(k, fours[k]) for k in fours], key = lambda x: -x[1])

print(letter_frequence)
print(pairs_frequence[:19])
print(repeat_pairs_frequence[:14])
print(triplets_frequence[:14])
print(fours_frequence[:10])

