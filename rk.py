class RabinKarp:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_length = len(text)
        self.pattern_length = len(pattern)
        self.prime = 101
        self.base = 256
        self.matches = []

    def search(self):
        pattern_hash = self._hash(self.pattern)
        text_hash = self._hash(self.text[:self.pattern_length])
        for i in range(self.text_length - self.pattern_length + 1):
            substring = self.text[i:i+self.pattern_length]
            if pattern_hash == text_hash and self._check_equal(i):
                self.matches.append(i)
            if i < self.text_length - self.pattern_length:
                text_hash = self._recalculate_hash(
                    self.text[i], self.text[i + self.pattern_length], text_hash)
        return self.matches

    def _hash(self, string):
        hash_value = 0
        for char in string:
            hash_value = (hash_value * self.base + ord(char)) % self.prime
        return hash_value

    def _recalculate_hash(self, old_char, new_char, old_hash):
        old_hash -= (ord(old_char) * pow(self.base, self.pattern_length - 1)) % self.prime
        old_hash = (old_hash * self.base) % self.prime
        old_hash = (old_hash + ord(new_char)) % self.prime
        return old_hash

    def _check_equal(self, index):
        for i in range(self.pattern_length):
            if self.pattern[i] != self.text[index + i]:
                return False
        return True

