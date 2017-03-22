# Automatic hangman puzzle solver for hirsipuutin
# https://github.com/gofore/hirsipuutin

import re


def getHitCounts(ws, ls):
    hits = {}
    for l in ls:
        for w in ws:
            if l in w:
                if l in hits:
                    hits[l] += 1
                else:
                    hits[l] = 1
    return hits

def findHitIndices(ch, w):
    inds = 0
    for i in w:
        inds = inds << 1
        if i == ch:
            inds += 1
    return inds

# returns what the expected value of len(remaining_words)
# is if letter l is guessed
def expectedRemaining(ws, l):
    hits_at = {}
    hit_count = 0
    for w in ws:
        if l in w:
            hit_count += 1
            hit_indices = findHitIndices(l, w)
            if hit_indices in hits_at:
                hits_at[hit_indices] += 1
            else:
                hits_at[hit_indices] = 1
    weighted_sum = 0
    for i, c in hits_at.items():
        weighted_sum += c * c/len(ws)
    misses = len(ws) - hit_count
    weighted_sum += misses * misses / len(ws)
    return weighted_sum

def findWordWith(ws, g):
    for i in range(len(ws)):
        if g in ws[i]:
            return i

def guess(ws, ls):
    # if less than 4 words left guess a whole word
    if len(ws) < 4:
        return ws.pop(0)
    weights = {}
    hit_counts = getHitCounts(ws, ls)
    for letter in ls:
        if letter not in hit_counts:
            continue
        else:
            hit_probability = hit_counts[letter]/len(ws)
            weights[letter] = expectedRemaining(ws, letter)-0.5*hit_probability

    g = min(weights, key=weights.get)
    # if there are only a couple of different word possibilities when
    # g is guessed guess a whole word instead of g
    if hit_counts[g] < 2:
        return ws.pop(findWordWith(ws, g))
    ls.remove(g)
    return g


print('andriamanitra')

# save words into lists by length
words = [[]]*100
word = input().strip()
while word:
    words[len(word)].append(word)
    word = input().strip()
letters = {letter for wordlist in words for word in wordlist for letter in word}

try:
    status = input()
    while status:
        remaining_words = words[len(status)]
        remaining_letters = letters.copy()
        g = ""

        while True:
            # remove all words that don't match regex
            if len(g) == 1:
                # make sure none of the wildcards are the letter that was guessed
                status = status.replace(".","[^"+g+"]")
            word_regex = re.compile(r"\A"+status+r"\Z", re.UNICODE)
            remaining_words = [w for w in remaining_words if word_regex.match(w)]

            # guess a letter or a word
            g = guess(remaining_words, remaining_letters)
            print(g)

            result = input()
            status = input()
            if result.startswith('MISS'):
                if len(g) == 1:
                    # remove all words that have the letter that missed
                    remaining_words = [w for w in remaining_words if w.find(g) < 0]

            if status.startswith('WIN') or status.startswith('LOSE') or not status:
                if status.startswith('WIN'):
                    # is this cheating? remove words that were already guessed
                    correct_word = status.split(" ")[2]
                    words[len(correct_word)].remove(correct_word)

                status = input()
                break
except EOFError:
    pass
