import re

def filter_verses_with_god(input_file, output_file):
    # Define divine keywords to search for
    keywords = ["God", "Lord", "Messiah", "Christ", "Jesus", "Father", "Jehovah"]

    # Compile a regex pattern for efficiency
    pattern = re.compile(rf"\b({'|'.join(keywords)})\b", re.IGNORECASE)

    # Read input file
    with open(input_file, "r", encoding="utf-8") as file:
        verses = file.readlines()

    # Normalize text by replacing NBSP and stripping whitespace
    normalized_verses = [verse.replace("\u00A0", " ").strip() for verse in verses]

    # Filter verses containing divine references
    filtered_verses = [
        verse for verse in normalized_verses if pattern.search(verse)
    ]

    # Write the filtered verses to the output file with proper line separation
    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(f"{verse}\n" for verse in filtered_verses)

    print(f"Filtered {len(filtered_verses)} verses mentioning God. Results saved to {output_file}.")

# Input and output file paths
input_file = "Nephi_verses.txt"  # Replace with your file name
output_file = "verses_with_god.txt"

# Run the function
filter_verses_with_god(input_file, output_file)
