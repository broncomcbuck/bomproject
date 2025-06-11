import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the GPT-J model and tokenizer
def load_model():
    model_name = "EleutherAI/gpt-j-6B"
    print("Loading GPT-J model. This might take a while...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        device_map="auto"  # CPU-based processing
    )
    print("Model loaded successfully!")
    return model, tokenizer

# Predict speaker with additional metadata and context
def predict_speaker(verse_text, book, chapter, prev_verse=None, next_verse=None, max_length=50):
    prompt = (
        f"In the book {book}, chapter {chapter}, determine the speaker of the following verse.\n"
        "Use the context of surrounding verses and metadata to identify the speaker accurately.\n\n"
    )
    if prev_verse:
        prompt += f"Previous verse: \"{prev_verse}\"\n"
    prompt += f"Current verse: \"{verse_text}\"\n"
    if next_verse:
        prompt += f"Next verse: \"{next_verse}\"\n"
    prompt += "Speaker:"

    # Tokenize and prepare input for the model
    inputs = tokenizer(prompt, return_tensors="pt")
    input_length = inputs.input_ids.shape[1]

    # Generate output
    outputs = model.generate(
        **inputs,
        max_length=input_length + max_length,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True
    )

    # Decode and extract the speaker
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    speaker = generated_text.split("Speaker:")[-1].strip().split("\n")[0]
    return speaker or "Unknown"

# Process verses and predict speakers
def process_verses(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in:
        verses = [line.strip() for line in f_in if line.strip()]

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for i, line in enumerate(verses):
            parts = line.split('    ', 1)
            if len(parts) < 2:
                continue

            ref, verse_text = parts
            book, chapter_verse = ref.split(" ", 1)
            chapter = chapter_verse.split(":")[0]

            # Include previous and next verse for context
            prev_verse = verses[i - 1].split('    ', 1)[1] if i > 0 else None
            next_verse = verses[i + 1].split('    ', 1)[1] if i < len(verses) - 1 else None

            # Predict speaker
            speaker = predict_speaker(verse_text, book, chapter, prev_verse, next_verse)

            # Write the results
            f_out.write(f"{ref}\t{speaker}\t{verse_text}\n")
            print(f"{ref}: Speaker predicted as {speaker}")

if __name__ == "__main__":
    # File paths
    input_file = "scriptures.txt"
    output_file = "verses_with_speakers_gptj.txt"

    # Load the model
    model, tokenizer = load_model()

    # Process the verses
    print("Starting speaker attribution with GPT-J...")
    process_verses(input_file, output_file)
    print(f"Speaker attribution completed. Results saved to {output_file}")
