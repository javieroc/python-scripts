import sys
import json
import csv
import os

# Create file
open('after.csv', 'a').close()
# os.mknod('after.csv')

# Read config file
with open('config.json', 'r') as file:
  loaded_json = json.load(file)

# Check config
if loaded_json['customer_id'] == "":
  sys.exit("please add match for customer_id")
if loaded_json['order_date'] == "":
  sys.exit("please add match for order_date")
if loaded_json['order_id'] == "":
  sys.exit("please add match for order_id")
if loaded_json['gross_unit_value'] == "" and loaded_json['gross_total_value'] == "":
  sys.exit("please add match for gross_unit_value or gross_total_value")

# Read input csv file
with open('before.csv') as csvfile:
  reader = csv.DictReader(csvfile)

  # Open results file
  with open('after.csv', 'w') as csvfile2:
    writer = csv.DictWriter(csvfile2, loaded_json.keys())
    writer.writeheader()

    for row in reader:
      new_row = {}

      # Rules.
      if row[loaded_json['customer_id']] in (None, ""): continue
      if row[loaded_json['order_date']] in (None, ""): continue
      if row[loaded_json['order_id']] in (None, ""): continue

      default_qty = 1
      # Create new row.
      for field in loaded_json:
        if loaded_json[field] is not "":

          if (row[loaded_json[field]] in (None, "")
            and field == "gross_unit_qty"
            and (row[loaded_json['sku']] in (None, "") or loaded_json['sku'] == "")
            and (row[loaded_json['product_id']] in (None, "") or loaded_json['product_id'] == "")):
            new_row["gross_unit_qty"] = default_qty
            continue

          if (field == "gross_total_value"
            and row[loaded_json['gross_total_value']] in (None, "")
            and row[loaded_json['gross_unit_value']] not in (None, "")):
            new_row["gross_total_value"] = row[loaded_json['gross_unit_value']] * new_row["gross_unit_qty"]
            continue

          if (field == "gross_unit_value"
            and row[loaded_json['gross_unit_value']] in (None, "")
            and row[loaded_json['gross_total_value']] not in (None, "")):
            new_row["gross_unit_value"] = row[loaded_json['gross_total_value']] / new_row["gross_unit_qty"]
            continue

          new_row[field] = row[loaded_json[field]]
        else:
          if field == "lob":
            new_row["lob"] = "ALL"
            continue

          new_row[field] = ""

      writer.writerow(new_row)
