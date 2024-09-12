import gzip
import os

def gzip_file(name, output_gz):
    with open(name, 'rb') as f_in:
        with open(output_gz, 'wb') as f_out:
            f_out.write(gzip.compress(f_in.read()))
    print(f"Gzipped file created: {output_gz}")

def split_file(file, part_size,name):
    file_size_bytes = os.path.getsize(file)
    part_size_bytes = part_size * 1024 * 1024  # Convert MB to Bytes

    if file_size_bytes <= part_size_bytes:
        print(f"Warning: {file} is less than {part_size}MB. Skipping splitting.")
        return
    part_num = 1
    with open(file, 'rb') as f:
        chunk = f.read(part_size_bytes)
        while chunk:
            part_file_name = f"{name}.part{part_num:03}"
            with open(part_file_name, 'wb') as part_file:
                part_file.write(chunk)
            print(f"Created: {part_file_name}")
            part_num += 1
            chunk = f.read(part_size_bytes)
def join_files(name):
    """Join part files into a single output file."""
    with open(name+".gz", 'wb') as outfile:
        part_num = 1
        while True:
            part_file = f"{name}.part{part_num:03}"
            if not os.path.exists(part_file):
                break  # No more parts
            print(f"Appending {part_file} to {name}")
            with open(part_file, 'rb') as infile:
                outfile.write(infile.read())
            part_num += 1
    with gzip.open(name+".gz", 'rb') as gzfile:
        with open(name, 'wb') as outfile:
            outfile.write(gzfile.read())
    
    print(f"Joined file created: {name}")
def main():
    action = input("Enter 's' to split or 'j' to join files: ").strip().lower()
    name = input("Enter File Name: ").strip().lower()

    if action == 'split' or action == 's':

        zipfile = f"{name}.gz"
        # Compress and split the file
        gzip_file(name, zipfile)
        split_file(zipfile, 25, name)  # Split into 25MB parts

    elif action == 'join' or action == 'j':

        # Join the split files
        join_files(name)

        # Optionally decompress the joined file
        # decompress_gzip(joined_output, part_prefix)

    else:
        print("Invalid action. Please enter 'split' or 'join'.")

if __name__ == "__main__":
    main()

# # Compress and split functions
# def gzip_file(input_file, output_gz):
#     """Compress the input file into a .gz file using gzip."""
#     with open(input_file, 'rb') as f_in:
#         with gzip.open(output_gz, 'wb') as f_out:
#             f_out.writelines(f_in)
#     print(f"Gzipped file created: {output_gz}")

# def split_file(file, part_size,name):
#     """Split the file into parts of the given size in MB if it's large enough."""
#     file_size_bytes = os.path.getsize(file)
#     part_size_bytes = part_size * 1024 * 1024  # Convert MB to Bytes

#     if file_size_bytes <= part_size_bytes:
#         print(f"Warning: {file} is less than {part_size}MB. Skipping splitting.")
#         return

#     part_num = 1
#     with open(file, 'rb') as f:
#         chunk = f.read(part_size_bytes)
#         while chunk:
#             part_file_name = f"{name}.part{part_num:03}"
#             with open(part_file_name, 'wb') as part_file:
#                 part_file.write(chunk)
#             print(f"Created: {part_file_name}")
#             part_num += 1
#             chunk = f.read(part_size_bytes)

# # Join and decompress functions
# def join_files(name):
#     """Join part files into a single output file."""
#     with open(name, 'wb') as outfile:
#         part_num = 1
#         while True:
#             part_file = f"{name}.part{part_num:03}"
#             if not os.path.exists(part_file):
#                 break  # No more parts
#             print(f"Appending {part_file} to {name}")
#             with gzip.open(part_file, 'rb') as infile:
#                 outfile.write(infile.read())
#             part_num += 1
#     print(f"Joined file created: {name}")



# # Main function to control the flow
# def main():
#     action = input("Enter 'split' to split or 'join' to join files: ").strip().lower()
    
#     if action == 'split' or action == 's':
#         input_file = input("Enter the path to the file you want to compress and split: ").strip()
#         output_gz = f"{input_file}.gz"
#         # Compress and split the file
#         gzip_file(input_file, output_gz)
#         split_file(output_gz, 25,input_file)  # Split into 25MB parts
    
#     elif action == 'join' or action == 'j':
#         part_prefix = input("Enter the prefix of the split files (e.g., 'file.gz'): ").strip()
        
#         # Join the split files
#         join_files(part_prefix)

#         # Optionally decompress the joined file
#         # decompress_gzip(joined_output, part_prefix)

#     else:
#         print("Invalid action. Please enter 'split' or 'join'.")

# if __name__ == "__main__":
#     main()
