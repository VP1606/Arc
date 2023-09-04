import os

os.system('pipreqs --force')

input_file = 'requirements.txt'
output_file = 'requirements.txt'

# Read the content of the input file
with open(input_file, 'r') as f:
    content = f.read()

# Split lines by newline character and extract package names
lines = content.strip().split('\n')
package_names = [line.split('==')[0] for line in lines]

# Write package names to the output file
with open(output_file, 'w') as f:
    for index, package_name in enumerate(package_names):
        f.write(package_name)
        if index < len(package_names) - 1:
            f.write('\n')

print("Package names extracted and written to", output_file)
