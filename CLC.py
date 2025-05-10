import re

def remove_url_from_line(line):
    url_pattern = r'https?://(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[^\s]*)?|(?:\.[a-z]{2,})(?:/[^\s]*)?'
    cleaned_line = re.sub(url_pattern, '', line)
    cleaned_line = cleaned_line.lstrip(':|').strip()
    return cleaned_line

def clean_combolist(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            cleaned_line = remove_url_from_line(line)
            outfile.write(cleaned_line + '\n')

input_file = 'input.txt'
output_file = 'output.txt'

clean_combolist(input_file, output_file)
print("Combolist cleaned successfully.")
