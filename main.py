import numpy as np

from bare_norvig import norvig_solution
from ngrams import look_forward, look_behind
from data import prep_data


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


def correction(word, candidates):
	dists = [levenstein_distance(word, c) for c in candidates]
	c = list(zip(candidates, dists))
	c.sort(key=lambda x: x[1], reverse=False)
	# TODO fix this shit
	print(c)
	return c[0][0]


def text_correction(text):
	text = text.lower().split()

	output = []

	for idx, word in enumerate(text):
		candidates = []

		# Base case - Norvig candidates
		norvig_candidates = norvig_solution(word)
		candidates.append(norvig_candidates)

		# Look forward
		if idx != len(text) - 1:
			forward_candidates = look_forward(word, text[idx + 1])
			candidates.extend(forward_candidates)

		# Look Behind
		if idx != 0:
			behind_candidates = look_behind(word, text[idx - 1])
			candidates.extend(behind_candidates)

		# TODO consider levenstein distance
		corrected = correction(word, candidates)
		output.append(corrected)

	return " ".join(output)


if __name__ == "__main__":
	prep_data()

	text = "this is my final message"
	output = text_correction(text)
	print("Corrected text:", end='\n\t')
	print(output)
