from data import INDIR_BIGRAM, DIR_BIGRAM
import numpy as np

TOP_K = 20



def levenstein_distance(word1, word2):
	w1_len = len(word1)
	w2_len = len(word2)

	lev = np.zeros((w1_len + 1, w2_len + 1), dtype=int)

	lev[:, 0] = np.arange(w1_len + 1)
	lev[0, :] = np.arange(w2_len + 1)

	for i in range(1, w1_len + 1):
		for j in range(1, w2_len + 1):
			m = 0
			if word1[i - 1] != word2[j - 1]:
				m = 1
			lev[i, j] = min(lev[i - 1, j] + 1, lev[i - 1, j - 1] + m, lev[i - 1, j] + 1)

	return lev[w1_len - 1, w2_len - 1].item()



def look_forward(word, next_word):
	global INDIR_BIGRAM
	if next_word not in INDIR_BIGRAM:
		return []

	prev_words = INDIR_BIGRAM[next_word]

	# max_candidates = min(len(INDIR_BIGRAM), TOP_K)
	# candidates = prev_words[:max_candidates]

	dists = [levenstein_distance(word, w) for w, _ in prev_words]
	prev_words = [(word, num/(d+1)) for d, (word, num) in zip(dists, prev_words)]

	candidates = sorted(prev_words, key=lambda x: x[1], reverse=True)[:TOP_K]

	candidates = [word for word, _ in candidates]
	return candidates

def look_behind(word, prev_word):
	global DIR_BIGRAM
	if prev_word not in DIR_BIGRAM:
		return []

	next_words = DIR_BIGRAM[prev_word]

	# max_candidates = min(len(DIR_BIGRAM), TOP_K)
	# candidates = next_words[:max_candidates]

	dists = [levenstein_distance(word, w) for w, _ in next_words]
	prev_words = [(word, num / (d+1)) for d, (word, num) in zip(dists, next_words)]

	candidates = sorted(prev_words, key=lambda x: x[1], reverse=True)[:TOP_K]

	candidates = [word for word, _ in candidates]
	return candidates