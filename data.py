import re
from collections import Counter


def find_words(text):
	return re.findall(r'\w+', text.lower())


VOCAB = Counter(find_words(open("data/big.txt").read()))
INDIR_BIGRAM = {}
DIR_BIGRAM = {}



def calc_probs(vocab):
	for key in vocab.keys():
		words = vocab[key].items()
		total = sum([num for _, num in words])
		words = list(map(lambda x: (x[0], x[1] / total), words))

		words.sort(key=lambda x: x[1], reverse=True)
		vocab[key] = words


def read_files():
	# Read first file
	data = []

	with open("data/bigrams.txt", "rb") as f:
		for byte_line in f:
			try:
				line = byte_line.decode("utf-8")
				data.append(line.strip())
			except UnicodeDecodeError:
				pass
	for line in data:
		occur, w1, w2 = line.split()
		occur = int(occur)
		w1, w2 = w1.lower(), w2.lower()

		if w1 not in DIR_BIGRAM.keys():
			DIR_BIGRAM[w1] = {}

		if w2 not in INDIR_BIGRAM.keys():
			INDIR_BIGRAM[w2] = {}

		DIR_BIGRAM[w1][w2] = occur
		INDIR_BIGRAM[w2][w1] = occur

	# Read second file
	data = []
	with open("data/coca_all_links.txt", "rb") as f:
		for byte_line in f:
			try:
				line = byte_line.decode("utf-8")
				data.append(line.strip())
			except UnicodeDecodeError:
				pass

	for line in data:
		line = line.split()
		occur, w1, w2 = int(line[0]), line[1].lower(), line[2].lower()

		if w1 not in DIR_BIGRAM.keys():
			DIR_BIGRAM[w1] = {}

		if w2 not in DIR_BIGRAM[w1].keys():
			DIR_BIGRAM[w1][w2] = 0

		DIR_BIGRAM[w1][w2] += occur

		if w2 not in INDIR_BIGRAM.keys():
			INDIR_BIGRAM[w2] = {}

		if w1 not in INDIR_BIGRAM[w2].keys():
			INDIR_BIGRAM[w2][w1] = 0

		INDIR_BIGRAM[w2][w1] += occur


def prep_data():
	global VOCAB
	VOCAB = Counter(find_words(open("data/big.txt").read()))
	read_files()

	calc_probs(DIR_BIGRAM)
	calc_probs(INDIR_BIGRAM)
