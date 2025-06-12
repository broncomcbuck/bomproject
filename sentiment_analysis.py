import re

def process_files_with_summary(input_files, output_file, god_keywords, positive_emotions, negative_emotions):
    # Compile regex for God-related keywords and emotions
    god_regex = re.compile(r'\b(' + '|'.join(map(re.escape, god_keywords)) + r')\b', re.IGNORECASE)
    pos_emo_regex = re.compile(r'\b(' + '|'.join(map(re.escape, positive_emotions)) + r')\b', re.IGNORECASE)
    neg_emo_regex = re.compile(r'\b(' + '|'.join(map(re.escape, negative_emotions)) + r')\b', re.IGNORECASE)

    # Strict inclusion: look for direct attribution of emotions to God
    emotion_attribution_patterns = [
        r'\b(' + '|'.join(map(re.escape, god_keywords)) + r')\b.*?\b(' + '|'.join(map(re.escape, positive_emotions + negative_emotions)) + r')\b',
        r'\b(' + '|'.join(map(re.escape, positive_emotions + negative_emotions)) + r')\b.*?\b(' + '|'.join(map(re.escape, god_keywords)) + r')\b',
        r'\b(' + '|'.join(map(re.escape, god_keywords)) + r')\b\'?s\b.*?\b(' + '|'.join(map(re.escape, positive_emotions + negative_emotions)) + r')\b'
    ]
    emotion_attribution_regex = re.compile('|'.join(emotion_attribution_patterns), re.IGNORECASE)

    # Output summary
    summary_lines = []

    for input_file in input_files:
        with open(input_file, 'r', encoding='utf-8') as f:
            verses = f.readlines()

        total_verses = len(verses)
        positive_verses = []
        negative_verses = []

        for verse in verses:
            verse = verse.replace('\u00A0', ' ').strip()  # Normalize NBSP

            # Ensure God-related keywords and direct attribution of emotions
            if god_regex.search(verse) and emotion_attribution_regex.search(verse):
                has_positive = pos_emo_regex.search(verse)
                has_negative = neg_emo_regex.search(verse)

                if has_positive:
                    positive_verses.append(verse)
                if has_negative:
                    negative_verses.append(verse)

        # Add results to the summary
        summary_lines.append(f"File: {input_file}")
        summary_lines.append(f"  Total verses: {total_verses}")
        summary_lines.append(f"  Positive emotion verses: {len(positive_verses)}")
        summary_lines.append(f"  Negative emotion verses: {len(negative_verses)}")
        summary_lines.append("")  # Blank line for readability

    # Write all results to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(summary_lines))
    print(f"Summary written to {output_file}")

# Keywords to look for (expanded list of God-related names)
god_keywords = [
    "Almighty", "Almighty God", "Alpha and Omega", "Being", "Beloved", "Beloved Son", "Christ",
    "Christ Jesus", "Christ the Son", "Counselor", "Creator", "Eternal Father", "Eternal God",
    "Eternal Head", "Eternal Judge", "Everlasting Father", "Everlasting God", "Father",
    "Father of heaven", "Father of heaven and of earth", "Founder of Peace", "God",
    "God of Abraham", "God of Abraham, and Isaac, and Jacob", "God of Abraham, and of Isaac, and the God of Jacob",
    "God of Isaac", "God of Israel", "God of Jacob", "God of miracles", "God of nature",
    "God of the whole earth", "Good shepherd", "Great Creator", "Great Spirit", "Head", "Holy Child",
    "Holy God", "Holy Messiah", "Holy One", "Holy One of Israel", "Holy One of Jacob", "Husband",
    "Immanuel", "Jehovah", "Jesus", "Jesus Christ", "Keeper of the gate", "King", "King of heaven",
    "Lamb", "Lamb of God", "Lord", "Lord God", "Lord God Almighty", "Lord God Omnipotent",
    "Lord God of Hosts", "Lord Jehovah", "Lord Jesus", "Lord Jesus Christ", "Lord of Hosts",
    "Lord of the Vineyard", "Lord Omnipotent", "Maker", "Man", "Master", "Mediator", "Messiah",
    "Mighty God", "Mighty One of Israel", "Mighty One of Jacob", "Most High", "Most High God",
    "Only Begotten of the Father", "Only Begotten Son", "Prince of Peace", "Prophet", "Redeemer",
    "Redeemer of Israel", "Redeemer of the world", "Rock", "Savior", "Savior Jesus Christ",
    "Savior of the world", "Shepherd", "Son", "Son of God", "Son of Righteousness",
    "Son of the Eternal Father", "Son of the Everlasting God", "Son of the Living God",
    "Son of the Most High God", "Stone", "Supreme Being", "Supreme Creator", "True and Living God",
    "True Messiah", "True Shepherd", "True Vine", "Well Beloved", "Wonderful"
]

# Expanded lists of emotions
positive_emotions = [
    "joy", "joys", "joyful", "rejoice", "rejoices", "rejoiced", "rejoicing",
    "happiness", "happy", "love", "loves", "loved", "loving", "peace", "peaceful",
    "delight", "delights", "delighted", "delighting", "compassion", "compassionate",
    "mercy", "merciful", "grace", "gracious", "hope", "hopeful", "bless", "blesses",
    "blessed", "blessing", "save", "saves", "saved", "saving", "redeem", "redeems",
    "redeemed", "redeeming"
]

negative_emotions = [
    "wrath", "wrathful", "anger", "angry", "grief", "grieves", "grieved", "grieving",
    "sorrow", "sorrowful", "lament", "laments", "lamented", "lamenting", "regret",
    "regrets", "regretted", "regretting", "displeasure", "displeased", "fury",
    "furious", "chasten", "chastens", "chastened", "chastening", "punish", "punishes",
    "punished", "punishing", "destroy", "destroys", "destroyed", "destroying",
    "condemn", "condemns", "condemned", "condemning"
]

# Files to process
input_files = ["Nephi_verses.txt", "Alma_verses.txt", "Mormon_verses.txt"]
output_file = "summary_output.txt"

# Process and summarize
process_files_with_summary(input_files, output_file, god_keywords, positive_emotions, negative_emotions)
