import re

def filter_emotions_attributed_to_god(input_file, output_positive, output_negative,
                                     god_keywords, positive_emotions, negative_emotions):
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

    positive_verses = []
    negative_verses = []

    with open(input_file, 'r', encoding='utf-8') as f:
        verses = f.readlines()

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

    with open(output_positive, 'w', encoding='utf-8') as fpos:
        fpos.write('\n'.join(positive_verses) + '\n')

    with open(output_negative, 'w', encoding='utf-8') as fneg:
        fneg.write('\n'.join(negative_verses) + '\n')

    print(f"Processed {input_file}")
    print(f"  Positive emotion verses: {len(positive_verses)}")
    print(f"  Negative emotion verses: {len(negative_verses)}")
    print()

# Keywords to look for
god_keywords = ["God", "Lord", "Messiah", "Christ", "Jesus", "Father", "Jehovah", "Holy One", "Redeemer", "King of Kings"]

positive_emotions = [
    "joy", "happiness", "love", "peace", "delight", "compassion",
    "mercy", "grace", "hope", "rejoices", "blesses", "saves", "redeems"
]

negative_emotions = [
    "wrath", "anger", "grief", "sorrow", "lament", "regret", "displeasure",
    "fury", "chastens", "punishes", "destroys", "condemns"
]

# Files to process
files = [
    ("Nephi_verses.txt", "Nephi_positive.txt", "Nephi_negative.txt"),
    ("alma_verses.txt", "Alma_positive.txt", "Alma_negative.txt"),
    ("mormon_verses.txt", "Mormon_positive.txt", "Mormon_negative.txt"),
]

for input_file, output_pos, output_neg in files:
    filter_emotions_attributed_to_god(input_file, output_pos, output_neg,
                                     god_keywords, positive_emotions, negative_emotions)
