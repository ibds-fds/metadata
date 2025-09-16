import os
import re

def split_turtle_file(input_file, output_dir, prefix_lines=None):
    """
    Split a Turtle file into chunks and create a catalog index.
    
    Args:
    input_file (str): Path to the input Turtle file
    output_dir (str): Directory to save the split files
    prefix_lines (list): Optional lines to add at the start of each output file
    
    Returns:
    list: List of generated filenames
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Default to empty list if no prefix provided
    prefix_lines = prefix_lines or []
    
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into chunks by blank lines
    chunks = content.split('\n\n')
    
    # Store generated filenames
    generated_files = []
    
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
        generated_files.append(filename)
    
    # Create catalog index
    create_catalog_index(output_dir, generated_files)
    
    return generated_files

def create_catalog_index(output_dir, generated_files):
    """
    Create a catalog index Turtle file referencing all generated files.
    
    Args:
    output_dir (str): Directory containing the split files
    generated_files (list): List of generated filenames
    """
    catalog_content = []
    
    # Prefixes
    catalog_content.append('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .')
    catalog_content.append('@prefix dcat: <http://www.w3.org/ns/dcat#> .')
    catalog_content.append('@prefix dcterms: <http://purl.org/dc/terms/> .')
    catalog_content.append(f'@base <https://federatief.datastelsel.nl/sectorregistraties/catalog> .')
    catalog_content.append('')
    
    # Catalog definition
    catalog_content.append('<> a dcat:Catalog ;')
    catalog_content.append('    dcterms:title "Sectorregistraties Catalog" ;')
    catalog_content.append('    dcat:dataset (')
    
    # Add datasets
    for filename in generated_files:
        catalog_content.append(f'        <https://github.com/ibds-fds/metadata/raw/refs/heads/main/datasets/{filename}.ttl>')
    
    catalog_content.append('    ) .')
    
    # Add individual dataset definitions
    for filename in generated_files:
        catalog_content.append(f'\n<{filename}> a dcat:Dataset ;')
        catalog_content.append(f'    dcterms:identifier "{filename}" .')
    
    # Write catalog index
    catalog_path = os.path.join(output_dir, 'sectorregistraties.ttl')
    with open(catalog_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(catalog_content) + '\n')
    
    print(f"Created catalog index at {catalog_path}")

# Example usage
if __name__ == "__main__":
    input_file = './src/sectorregistraties.ttl'
    output_dir = './datasets'
    
    # Example prefix lines (modify as needed)
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
