class RabinKarp:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_length = len(text)
        self.pattern_length = len(pattern)
        self.prime = 101
        self.base = 256
        self.matches = []

    def search(self, limit=None):
        pattern_hash = self._hash(self.pattern)
        text_hash = self._hash(self.text[:self.pattern_length])
        match_count = 0  # Initialize match count
        for i in range(self.text_length - self.pattern_length + 1):
            substring = self.text[i:i+self.pattern_length]
            if pattern_hash == text_hash and self._check_equal(i):
                self.matches.append(i)
                match_count += 1
                if limit is not None and match_count >= limit:
                    break  # Stop searching if limit is reached
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


def main():
    while True:
        text = input("\nEnter the text: ")
        pattern = input("\nEnter the pattern to search for: ")
        limit = int(input("\nEnter the maximum number of matches to display: "))  # Prompt user for limit

        rk = RabinKarp(text, pattern)
        matches = rk.search(limit=limit)  # Pass limit to search method

        if matches:
            print(f"\nPattern found at positions: {matches}")
            print(f"\nNumber of matches found: {len(matches)}")
        else:
            print("Pattern not found")

        choice = input("\nDo you want to continue? (yes/no): ")
        if choice.lower() != "yes":
            print("Exiting program...")
            break


if __name__ == "__main__":
    main()
