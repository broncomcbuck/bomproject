import re  # Import the regular expression library

# Step 1: Load the text file
with open('scriptures.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Step 2: Split the text into verses
# Use a regular expression to capture book names, chapter:verse, and the verse content
verse_pattern = r'([1-3]?\s?[A-Za-z]+\s\d+:\d+)\s+(.*)'

# Find all verses using the pattern
verses = re.findall(verse_pattern, text)

# Print total verses found
print(f"Total verses: {len(verses)}")

# Step 3: Find verses about God
keywords = ['God', 'Lord', 'Jesus', 'merciful', 'eternal', 'just']
god_passages = [
    f"{ref} {content}"
    for ref, content in verses
    if any(keyword.lower() in content.lower() for keyword in keywords)
]

print(f"Passages about God: {len(god_passages)}")

# Step 4: Save the results
with open('god_passages_manual.txt', 'w', encoding='utf-8') as file:
    for passage in god_passages:
        file.write(passage + '\n')  # Write each passage on a new line

print("Passages about God saved to 'god_passages_manual.txt'")
