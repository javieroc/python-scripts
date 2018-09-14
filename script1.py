import json
import csv
import os

# Create file
open('after.csv', 'a').close()
# os.mknod('after.csv')

# Read config file
with open('config.json', 'r') as file:
  loaded_json = json.load(file)

# Read input csv file
with open('before.csv') as csvfile:
  reader = csv.DictReader(csvfile)

  # Open results file
  with open('after.csv', 'w') as csvfile2:
    writer = csv.writer(csvfile2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Write header.
    header = []
    for field in loaded_json:
      if (loaded_json[field] is not ""):
        header.append(loaded_json[field])
    writer.writerow(header)

    for row in reader:
      new_row = []

      # Rules.
      if row[loaded_json['customer_id']] in (None, ""): continue
      if row[loaded_json['order_date']] in (None, ""): continue
      if row[loaded_json['order_id']] in (None, ""): continue

      # Create new row.
      for field in loaded_json:
        if (loaded_json[field] is not ""):
          new_row.append(row[loaded_json[field]])

      writer.writerow(new_row)
