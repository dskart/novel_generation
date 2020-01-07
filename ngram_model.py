import re
import random
import math


def tokenize(text):
    return re.findall(r"[\w]+|[^\s\w]", text)


def ngrams(n, tokens):
    tokens_with_pads = ["<START>"]*(n-1) + tokens + ["<END>"]

    n_gram = []
    for i, token in enumerate(tokens_with_pads):
        if i >= n-1:
            start_index = i-n+1
            n_gram.append((tuple(tokens_with_pads[start_index:i]), token))

    return n_gram


class NgramModel(object):

    def __init__(self, n):
        self._n = n
        self._token_for_context_counter = {}
        self._context_counter = {}

    def update(self, sentence):
        for current_context, token in ngrams(self._n, tokenize(sentence)):
            self._update_context_counter(current_context)
            self._update_token_for_context_counter(current_context, token)

        return

    def _update_context_counter(self, current_context):
        if current_context in self._context_counter:
            self._context_counter[current_context] += 1
        else:
            self._context_counter[current_context] = 1

    def _update_token_for_context_counter(self, current_context, token):
        if current_context in self._token_for_context_counter:

            if token in self._token_for_context_counter[current_context]:
                self._token_for_context_counter[current_context][token] += 1
            else:
                self._token_for_context_counter[current_context][token] = 1

        else:
            self._token_for_context_counter[current_context] = {token: 1}

    def prob(self, context, token):
        if context in self._token_for_context_counter and token in self._token_for_context_counter[context]:
            return self._average(self._token_for_context_counter[context][token], self._context_counter[context])

        return 0

    def _average(self, a, b):
        return float(a) / b

    def random_token(self, context):
        r = random.random()
        if context in self._context_counter:
            tokens_for_context = sorted(
                self._token_for_context_counter[context].keys())

            left_proba = 0
            right_proba = 0
            for token in tokens_for_context:
                right_proba += self.prob(context, token)
                if left_proba <= r < right_proba:
                    return token

                left_proba += self.prob(context, token)

        return None

    def random_text(self, token_count):
        if self._n == 1:
            tokens = self._find_token_from_no_context(token_count)
        else:
            tokens = self._find_token_from_context(token_count)

        return " ".join(tokens)

    def _find_token_from_no_context(self, token_count):
        tokens = []
        for __ in range(token_count):
            tokens.append(self.random_token(()))

        return tokens

    def _find_token_from_context(self, token_count):
        tokens = []
        current_context = ("<START>",) * (self._n-1)
        for __ in range(token_count):
            current_token = self.random_token(current_context)
            tokens.append(current_token)

            if current_token == "<END>":
                current_context = ("<START>",) * (self._n-1)
            else:
                current_context = current_context[1:] + (current_token,)

        return tokens

    def perplexity(self, sentence):
        product = 0
        tokens = tokenize(sentence)

        for current_context, token in ngrams(self._n, tokens):
            product += math.log(self.prob(current_context, token))

        return (1/math.exp(product)) ** (float(1)/(len(tokens)+1))


def create_ngram_model(n, path):
    ngram = NgramModel(n)

    with open(path) as f:
        for line in f:
            ngram.update(line)

    return ngram
