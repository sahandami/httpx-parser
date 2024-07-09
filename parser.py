import json
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_possible_fields(file_path):
    try:
        with open(file_path, 'r') as file:
            first_entry = json.loads(file.readline())
            possible_fields = list(first_entry.keys())
            print("Possible fields:", ", ".join(possible_fields))
    except Exception as e:
        print(f"Error reading JSON file: {e}")

def parse_httpx_output(file_path, fields, sort_fields=None):
    try:
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return
    
    parsed_data = []
    for entry in data:
        parsed_entry = [entry.get(field, 'N/A') for field in fields]
        parsed_data.append(parsed_entry)
    
    if sort_fields:
        # Sort the data based on the specified fields
        sort_indices = []
        for sort_field in sort_fields:
            try:
                sort_indices.append(fields.index(sort_field))
            except ValueError:
                print(f"Sort field {sort_field} not found in fields")
                return

        # Sort using multiple keys
        parsed_data.sort(key=lambda x: tuple(x[idx] for idx in sort_indices))
    
    # Define colors for different fields
    color_mapping = {
        'url': Fore.GREEN,
        'status_code': Fore.YELLOW,
        'content_length': Fore.BLUE,
        'location': Fore.CYAN,
        'cdn': Fore.MAGENTA
    }
    
    # Print the output
    for entry in parsed_data:
        colored_entry = []
        for i, e in enumerate(entry):
            field = fields[i]
            color = color_mapping.get(field, Fore.WHITE)
            colored_entry.append(f"{color}[{e}]")
        print(' '.join(colored_entry))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parser.py <file_path> <fields...> [-s <sort_field>...] [-h]")
        sys.exit(1)

    if '-h' in sys.argv:
        file_path = sys.argv[1]
        print_possible_fields(file_path)
        sys.exit(0)

    file_path = sys.argv[1]
    if '-s' in sys.argv:
        sort_field_index = sys.argv.index('-s')
        sort_fields = sys.argv[sort_field_index + 1:]
        fields = sys.argv[2:sort_field_index]
    else:
        sort_fields = None
        fields = sys.argv[2:]

    parse_httpx_output(file_path, fields, sort_fields)
