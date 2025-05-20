import gzip
import os
import subprocess

def modify_vcf(input_vcf:str, output_vcf:str)->None:
    
    """
    Modify a VCF file by replacing a specific string and write the result to a new file.
    This function reads a gzipped VCF file, replaces all occurrences of the string
    "HGMD-PUBLIC_20204" with "HGMD_PUBLIC_20204", and writes the modified content
    to a new output file.
    Args:
        input_vcf (str): The path to the input gzipped VCF file.
        output_vcf (str): The path to the output file where the modified VCF content will be written.
    Returns:
        None
    """
    
    with gzip.open(input_vcf, 'rt') as infile, open(output_vcf, 'w') as outfile:

        for line in infile:
            # Change "HGMD-PUBLIC_20204" to "HGMD_PUBLIC_20204"
            modified_line = line.replace("HGMD-PUBLIC_20204", "HGMD_PUBLIC_20204")
            # Write the modified line to the output file
            outfile.write(modified_line)
    
    pass

def process_vcf_files(original_folder:str, processed_folder:str)->None:
    
    """
    Processes VCF files from the original folder, modifies them, compresses them with bgzip, 
    and indexes them with bcftools, then saves the processed files to the processed folder.
    Args:
        original_folder (str): The path to the folder containing the original VCF files.
        processed_folder (str): The path to the folder where the processed VCF files will be saved.
    Returns:
        None
    """

    list_dir = os.listdir(original_folder)

    gz_file = [file for file in list_dir if file.split('.')[-1]=='gz']

    for file in gz_file:
        modify_vcf(
            input_vcf=os.path.join(original_folder, file),
            output_vcf=os.path.join(processed_folder, file[:-3])
        )

        bgzip_cmd = ['bgzip', '-c', os.path.join(processed_folder, file[:-3])]
        with open(os.path.join(processed_folder, file), 'wb') as out_file:
            subprocess.run(bgzip_cmd, stdout=out_file, check=True)

        bcf_cmd = ['bcftools', 'index', os.path.join(processed_folder, file)]
        subprocess.run(bcf_cmd, check=True)
    
    pass


original_dir = 'path/to/original/vcf/files'
modified_dir = 'path/to/modified/vcf/files'

process_vcf_files(original_dir, modified_dir)