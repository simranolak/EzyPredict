#!/usr/bin/env python
# coding: utf-8

# In[50]:


import pandas as pd
import os
import requests
import subprocess
import time
import re
import xmltramp2


# ## ORF <> UniProt mapping file and functon to convert ORF ids from metabolic model to uniprot IDs

# In[51]:


GenProt_SGD = pd.read_csv('uniprot_allScerevisiae_20230208.tsv', 
                          sep="\t")[["Entry", 
                                     "Gene Names (ordered locus)",
                                     "Gene Names (primary)",
                                     "Annotation"]].drop_duplicates()
GenProt_SGD.columns = ["Uniprot.ID", "ORF", "Gene.Name", "Uniprot.Annotation.Score"]
# Convert multiple ORF names into multiple rows
ORFs2bind = []

for idx, row in GenProt_SGD.iterrows():
    if isinstance(row["ORF"], str):  # Check if the value is a string before split
        orfs = [orf.strip() for orf in row["ORF"].split(';')]
        if len(orfs) > 1:
            ORFs2bind.extend([{
                "Uniprot.ID": row["Uniprot.ID"],
                "ORF": orf,
                "Gene.Name": row["Gene.Name"],
                "Uniprot.Annotation.Score": row["Uniprot.Annotation.Score"]
            } for orf in orfs[1:]])
            GenProt_SGD.at[idx, "ORF"] = orfs[0]

ORFs2bind_df = pd.DataFrame(ORFs2bind)
GenProt_SGD = pd.concat([GenProt_SGD, ORFs2bind_df], ignore_index=True)
# Convert multiple gene names into multiple rows
genes2bind = []

for idx, row in GenProt_SGD.iterrows():
    if isinstance(row["Gene.Name"], str):  # Check if the value is a string before split
        genes = row["Gene.Name"].split(';')
        if len(genes) > 1:
            genes2bind.extend([{
                "Uniprot.ID": row["Uniprot.ID"],
                "ORF": row["ORF"],
                "Gene.Name": gene,
                "Uniprot.Annotation.Score": row["Uniprot.Annotation.Score"]
            } for gene in genes[1:]])
            GenProt_SGD.at[idx, "Gene.Name"] = genes[0]

genes2bind_df = pd.DataFrame(genes2bind)
GenProt_SGD = pd.concat([GenProt_SGD, genes2bind_df], ignore_index=True)

GenProt_SGD['ORF'] = GenProt_SGD['ORF'].where(GenProt_SGD['ORF'] != "", float('nan'))
GenProt_SGD['Gene.Name'] = GenProt_SGD.apply(lambda row: (row['ORF'] if isinstance(row['ORF'], str) else "").strip() 
                                            if (isinstance(row['Gene.Name'], str) and row['Gene.Name'].strip() == "") 
                                            else (row['Gene.Name'] if isinstance(row['Gene.Name'], str) else "").strip(), 
                                            axis=1)

# Function to convert UniprotIDs to ORFs
def convert_ORF2Uniprot(orf_name):
    uniprot_id = GenProt_SGD[GenProt_SGD["ORF"] == orf_name]["Uniprot.ID"].iloc[0] if any(GenProt_SGD["ORF"] == orf_name) else None
    return uniprot_id


# ## Function for passing a UniProt ID to the Uniprot API and getting a sequence back

# In[52]:


# define a function for fetching uniprot sequences 

def fetch_sequence_from_uniprot(uniprot_id):
    base_url = "https://www.uniprot.org/uniprot/"
    url = base_url + uniprot_id + ".fasta"
    response = requests.get(url)
    
    if response.status_code == 200:
        fasta_data = response.text
        # Extract the sequence data (without FASTA header)
        sequence = "".join(fasta_data.split('\n')[1:])
        return sequence
    else:
        print(f"Failed to retrieve data for UniProt ID: {uniprot_id}")
        return None


# ## Function that uses the ESM2 model to encode the protein sequence

# In[53]:


def encode_sequence_with_ESM2(sequence):
    # Prepare the data for ESM2
    data = [(sequence, sequence)]
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    
    # Get the representations.
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[33])
        token_representations = results["representations"][33]
    
    # For many tasks, you might want to consider the average of all token representations in the sequence.
    avg_representation = token_representations.mean(1)
    
    return avg_representation


# # Pepstats functions

# ## Functions to submit an amino acid sequence, check if job is done and retrieve the job results to disk 

# In[55]:


def submit_sequence(sequence, email='simran.aulakh@well.ox.ac.uk'):
    # Submit sequence and get job ID
    cmd = ["python", "pepstats_module.py", "--asyncjob", "--email", email, "--sequence", sequence]
    output = subprocess.check_output(cmd).decode().strip()
    
    # Extract the job ID using a regular expression
    match = re.search(r'(emboss_pepstats-[^\s]+)', output)
    if match:
        job_id = match.group(1)
    else:
        raise ValueError("Unable to extract job ID from the output.")
    
    return job_id

def is_job_done(job_id):
    #  check job status
    cmd = ["python", "pepstats_module.py", "--status", "--jobid", job_id]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Check if the job is finished by inspecting the result output
    if "FINISHED" in result.stdout: 
        return True
    return False

def retrieve_job_results(job_id, outfile):
    # check job is done
    if is_job_done(job_id):
        cmd = ["python", "pepstats_module.py", "--polljob", "--jobid", job_id, "--outfile", outfile]
        subprocess.run(cmd)
    else:
        print("Job is not finished yet.")


# ## Function to read the job results files written to disk for all results in the pepstats_results folder and turn them into one dataframe

# In[56]:

def parse_pepstats(file_path):
    data = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()

        # Parse the total residue number from the header
        header = lines[0].strip()
        index_of_to = header.split().index("to")
        total_residues = int(header.split()[index_of_to + 1])

        for line in lines:
            if any(keyword in line for keyword in [ "Residues", "Charge", "Isoelectric Point", "A280 Molar", "Improbability"]):
                key_value = line.split('=')
                if len(key_value) < 2:  # Check to make sure there is both a key and a value
                    continue
                key = key_value[0].strip()
                value = key_value[1].split()[0]

                # Ensure the "Residues" value matches the header value
                if key == "Residues" and int(value) != total_residues:
                    raise ValueError(f"Residue count mismatch in {file_path}!")

                data[key] = value
                
        # Extracting property information at the end of the file
        start_index = next((i for i, line in enumerate(lines) if 'Property' in line), None)
        if start_index:
            for line in lines[start_index+1:]:
                parts = line.strip().split()
                if len(parts) >= 3:
                    data[parts[0]] = parts[2]

        # Add total residues to the data dictionary
        data["Total Residues"] = total_residues

    return data


### Function to take all pepstats result files in the pepstats_results folder, parse them and covnert them into one pandas df
def collate_pepstats_to_dataframe(directory='.'):
    all_data = []
    file_paths = [f for f in os.listdir(directory) if f.endswith('_pepstats.out.txt')]

    for file_name in file_paths:
        full_file_path = os.path.join(directory, file_name)
        data = parse_pepstats(full_file_path)
        uniprot_id = file_name.split('_')[0]
        all_data.append((uniprot_id, data))

    # Convert list of dictionaries to dataframe
    df = pd.DataFrame.from_dict(dict(all_data), orient='index')
    
    return df