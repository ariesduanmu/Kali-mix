import sys
sys.path.append('../')
from utility import *

def get_key():
	f1 = read_file("found1")
	f2 = read_file("found2")

	strs = [[f1[j] for j in range(len(f1)) if j % 6 == i]\
	         + [f2[j] for j in range(len(f2)) if j % 6 == i] for i in range(6)]
	key = [get_single_key(strs[i]) for i in range(6)]
	return key


if __name__ == "__main__":
	key = get_key()
	k5 = read_file("krypton5")
	print(decrypt(k5, key))


