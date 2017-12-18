
#https://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html
englishLetterFreq = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
most_common_pairs = ['TH', 'EA', 'OF', 'TO', 'IN', 'IT', 'IS', 'BE', 'AS', 'SO', 'WE', 'HE', 'BY', 'OR', 'ON', 'DO', 'IF', 'ME', 'UP']
most_common_repeat = ['SS', 'EE', 'TT', 'FF', 'LL', 'MM', 'OO']
most_common_triplets = ['THE','EST','FOR','AND','HIS','ENT','THA']

def read_file(filename):
	return open(filename, 'r').read().strip('\n').replace(' ','')
'''
   ***********************************
   *They are work for Vigebere cipher*
   ***********************************
'''

def gcd(a,b):
	while b > 0:
		tmp = a % b
		a = b
		b = tmp
	return a

# One way to findout the cipher length
def kasiski(text):
	dic = {}
	for i in range(len(text)-2):
		for j in range(i+3,len(text)):
			ciphertext_piece = text[i:j]
			if ciphertext_piece in dic:
				dic[ciphertext_piece] += [i]
			else:
				dic[ciphertext_piece] = [i]
	ciphertext_pieces = sorted([[k, dic[k]] for k in dic], key=lambda x: -len(x[1]))
	print(ciphertext_pieces[:10])
	c = ciphertext_pieces[0][1]
	if c[0] == 0:
		g = c[1]
		k = 2
	else:
		g = c[0]
		k = 1

	for i in range(k,len(c)):
		g = gcd(g,c[i])
	return g


def letter_frequence(text):
	fq = [0 for _ in range(26)]
	for t in text:
		i = ord(t.upper()) - ord('A')
		fq[i] += 1
	return fq

#Second way for cipher length
def coincidence(text, m):
	c_index = lambda frequences, n: \
	          sum(frequences[i] * (frequences[i] - 1) for i in range(26)) / (n * (n - 1))
	deviations = []
	for i in range(1,m+1):
		t = [text[j::i] for j in range(i)]
		indexs = []
		for j in range(len(t)):
			fq = letter_frequence(t[j])
			indexs.append(c_index(fq, len(t[j])))
		deviations.append([i,deviation(indexs)])
		print(indexs)
	
	return min(deviations, key = lambda x: x[1])[0]


def deviation(indexs):
	# this magic_num is in normal English the frquences squar of letters
	magic_num = 0.065
	return sum([pow((i - magic_num),2) for i in indexs]) / len(indexs)

if __name__ == "__main__":
	text = read_file('test')
	print(coincidence(text,20))


