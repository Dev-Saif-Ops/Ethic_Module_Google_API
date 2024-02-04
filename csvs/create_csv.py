import csv
import random

# Create a CSV file with random data
rows = 5
columns = 10
csv_file = 'Your_file_name.csv'

with open(csv_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write header
    header = [f'Column_{i}' for i in range(1, columns + 1)]
    csv_writer.writerow(header)

    # Write random data
    for _ in range(rows):
        row_data = [random.randint(1, 100) for _ in range(columns)]
        csv_writer.writerow(row_data)

print(f'CSV file "{csv_file}" created successfully.')

