#!/usr/bin/env python3
import argparse
import re
import sys

def utf8_to_url_encoding(text, add_quotes=False, include_pattern=None):
    hex_parts = []
    should_encode_all = include_pattern is None  # If no --include, encode everything

    for char in text:
        utf8_bytes = char.encode('utf-8')

        if should_encode_all or (include_pattern and re.match(include_pattern, char)):
            encoded_char = ''.join(f"%{b:02x}" for b in utf8_bytes)  # Encode matching chars
        else:
            encoded_char = char  # Keep non-matching characters unchanged

        hex_parts.append(encoded_char)
    
    if add_quotes:
        outstr = '"' + ''.join(hex_parts) + '"'
    else:
        outstr = ''.join(hex_parts)

    return outstr

def main():
    parser = argparse.ArgumentParser(description="Convert UTF-8 text to URL encoding with optional filtering.")
    
    parser.add_argument("--include-quotes", action="store_true", help="Always encode quotes as %22 or %27")
    parser.add_argument("--include", type=str, help="Regex pattern to determine which characters should be URL-encoded")
    parser.add_argument("text", nargs="?", help="The text to convert (or leave empty to read from stdin)")

    args = parser.parse_args()

    # Read from stdin if no text is provided
    input_text = args.text if args.text else sys.stdin.read().strip()

    # Process text with filters
    encoded_output = utf8_to_url_encoding(input_text, args.include_quotes, args.include)
    
    print(encoded_output)

if __name__ == "__main__":
    main()
