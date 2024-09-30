import os
import pandas as pd
import pefile

def extract_pe_header(file_path, num_bytes=1024):
    try:
        pe = pefile.PE(file_path)
        # Extract the first num_bytes of the PE header
        pe_header = pe.write()[0:num_bytes] 
        return pe_header
    except pefile.PEFormatError as pe:
        print(f"cant open  file error: {pe}")
        return None
    except Exception as e:
        print(f"this error occured: {e}")
        return None

def process_folder(folder_path, label):
    data = []
    for filename in os.listdir(folder_path):
        #if filename.endswith('.exe'):
        file_path = os.path.join(folder_path, filename)
        pe_header = extract_pe_header(file_path)
        if pe_header:
            row = {
                 'GR': label
                }
            # Add PE header bytes as individual columns
            for i in range(1024):
                row[i] = pe_header[i]
            data.append(row)
    return data

def main():
    goodware_folder = 'goodware'
    malware_folder = 'malware'

    goodware_data = process_folder(goodware_folder, 0) 
    malware_data = process_folder(malware_folder, 1)

    all_data = goodware_data + malware_data
    df = pd.DataFrame(all_data)
    
    # Save DataFrame to CSV file
    csv_file_path = 'pe_headers.csv'
    df.to_csv(csv_file_path, index=False)
    print(f'Data saved to {csv_file_path}')

if __name__ == "__main__":
    main()
