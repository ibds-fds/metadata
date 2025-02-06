import os
import re

def split_turtle_file(input_file, output_dir, prefix_lines=None):
    """
    Split a Turtle file into chunks based on blank line separation.
    Use the first line's UUID as the output filename.
    
    Args:
    input_file (str): Path to the input Turtle file
    output_dir (str): Directory to save the split files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into chunks by blank lines
    chunks = content.split('\n\n')
    
    # Process each chunk
    for chunk in chunks:
        # Skip empty chunks
        if not chunk.strip():
            continue
        
        # Get the first line (should contain UUID)
        first_line = chunk.split('\n')[0].strip()
        
        # Extract UUID (assuming it's a valid filename-friendly identifier)
        filename_match = re.match(r'^dataset:([\w-]+)', first_line)
        if filename_match:
            filename = filename_match.group(1)
        else:
            # Fallback naming if no UUID found
            filename = 'chunk_' + str(hash(chunk))
        
        # Write chunk to file
        output_path = os.path.join(output_dir, f"{filename}.ttl")
        with open(output_path, 'w', encoding='utf-8') as out_f:
            # Write prefix lines first
            for prefix_line in prefix_lines:
                out_f.write(prefix_line + '\n')
            
            # Write the chunk
            out_f.write(chunk.strip() + '\n')        
        print(f"Created {output_path}")

# Example usage
if __name__ == "__main__":
    input_file = './src/sectorregistraties.ttl'
    output_dir = './datasets/split_datasets'
    prefix_lines = [
        '@prefix dataset: <http://data.overheid.nl/dataset/> .',
        '@prefix dcat:    <http://www.w3.org/ns/dcat#> .',
        '@prefix dcatap:  <http://data.europa.eu/r5r/> .',
        '@prefix dct:     <http://purl.org/dc/terms/> .',
        '@prefix foaf:    <http://xmlns.com/foaf/0.1/> .',
        '@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .',
        '@prefix sh:      <http://www.w3.org/ns/shacl#> .',
        '@prefix vcard:   <http://www.w3.org/2006/vcard/ns#> .',
        '@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .',
        ''
    ]
    split_turtle_file(input_file, output_dir, prefix_lines)