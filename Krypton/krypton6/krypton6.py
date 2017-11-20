import sys
sys.path.append('../')
from utility import *

def key_size():
	f1 = read_file("found1")
	f2 = read_file("found2")
	f3 = read_file("found3")

	commons = []
	#I guess less than 20...
	for size in range(1,20):
		max_s1, min_s1 = freq_in_size(f1, size)
		max_s2, min_s2 = freq_in_size(f2, size)
		max_s3, min_s3 = freq_in_size(f3, size)
		m = len(set(max_s1) & set(max_s2) & set(max_s3)) +\
		    len(set(min_s1) & set(min_s2) & set(min_s3))
		commons.append([m,size])
	return max(commons, key = lambda x: x[0])[1]

def freq_in_size(strings, size):
	freq = [[0,chr(ord('A')+i)] for i in range(26)]
	for i in range(0,len(strings),size):
		s = strings[i]
		freq[ord(s) - ord('A')][0] += 1
	freq = list(map(lambda x: x[1], sorted(freq, key = lambda x: -x[0])))
	return freq[:6], freq[-6:]

def get_key():
	f1 = read_file("found1")
	f2 = read_file("found2")
	f3 = read_file("found3")

	size = key_size()
	strs = [[f1[j] for j in range(len(f1)) if j % size == i]\
	         + [f2[j] for j in range(len(f2)) if j % size == i]\
	         +  [f3[j] for j in range(len(f3)) if j % size == i] for i in range(size)]
	key = [get_single_key(strs[i]) for i in range(size)]
	return key

if __name__ == "__main__":
	key = get_key()
	k6 = read_file("krypton6")
	print(decrypt(k6, key))
