from collections import defaultdict

# Using int as the default factory for counting
word_counts = defaultdict(int)
text = "this is a test this is only a test"
for word in text.split():
    word_counts[word] += 1
print(word_counts)

# Using list as the default factory for grouping
grouped_items = defaultdict(list)
data = [("apple", 1), ("banana", 2), ("apple", 3)]
for key, value in data:
    grouped_items[key].append(value)
print(grouped_items)