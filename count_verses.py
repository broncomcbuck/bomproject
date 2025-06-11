def count_verses(input_file, output_file):
    count = 0
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Strip whitespace
            line = line.strip()
            # Check if line starts with a verse reference pattern
            # Example pattern: "1 Nephi 1:1"
            # We'll check if line starts with a digit, then space, then word, then space, then chapter:verse
            # Simple heuristic: line starts with something like "1 Nephi 1:1"
            if line:
                parts = line.split(' ', 2)
                if len(parts) >= 2:
                    book = parts[0]
                    chapter_verse = parts[1]
                    # Check if chapter_verse contains a colon and is numeric before and after colon
                    if ':' in chapter_verse:
                        chap, verse = chapter_verse.split(':', 1)
                        if chap.isdigit() and verse.isdigit():
                            count += 1

    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(f"Total verses: {count}\n")

    print(f"Counted {count} verses. Result saved to {output_file}.")

if __name__ == "__main__":
    count_verses('Nephi_verses.txt', 'verse_count.txt')
