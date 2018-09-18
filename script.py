import sys
import getopt
import json
import csv
import os

def main():
  inputfile = 'before.csv'
  outputfile = 'after.csv'
  configfile = 'config.json'
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hc:i:o:", ["help", "config=", "ifile", "ofile"])
  except getopt.GetoptError as err:
    print(err)
    print('script.py -c <config> -i <inputfile> -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print ('script.py -c <config> -i <inputfile> -o <outputfile>')
      sys.exit()
    elif opt in ("-c", "--config"):
      configfile = arg
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg
    else:
      assert False, "unhandled option"    

  # Create file
  open(outputfile, 'a').close()
  # os.mknod('after.csv')

  # Read config file
  with open(configfile, 'r') as file:
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
  with open(inputfile) as csvfile:
    reader = csv.DictReader(csvfile)

    # Open results file
    with open(outputfile, 'w') as csvfile2:
      writer = csv.DictWriter(csvfile2, loaded_json.keys())
      writer.writeheader()

      for row in reader:
        new_row = {}

        # Rules.
        if row[loaded_json['customer_id']] in (None, ''):
          continue
        else:
          new_row['customer_id'] = row[loaded_json['customer_id']]

        if row[loaded_json['order_date']] in (None, ''):
          continue
        else:
          new_row['order_date'] = row[loaded_json['order_date']]

        if row[loaded_json['order_id']] in (None, ''):
          continue
        else:
          new_row['order_id'] = row[loaded_json['order_id']]

        if (loaded_json['lob'] is not ''):
          if (row[loaded_json['lob']] in (None, '')):
            continue
          else:
            new_row['lob'] = row[loaded_json['lob']]
        else:
          new_row['lob'] = 'All'

        if (loaded_json['gross_unit_qty'] is not '' and row[loaded_json['gross_unit_qty']] not in (None, '')):
          new_row['gross_unit_qty'] = row[loaded_json['gross_unit_qty']]
        else:
          new_row['gross_unit_qty'] = 1

        if (loaded_json['gross_total_value'] is not '' and row[loaded_json['gross_total_value']] not in (None, '')):
          new_row['gross_total_value'] = row[loaded_json['gross_total_value']]
        else:
          if (loaded_json['gross_unit_value'] is not '' and row[loaded_json['gross_unit_value']] not in (None, '')):
            new_row['gross_total_value'] = float(row[loaded_json['gross_unit_value']]) * float(new_row["gross_unit_qty"])
          else:
            continue

        if (loaded_json['gross_unit_value'] is not '' and row[loaded_json['gross_unit_value']] not in (None, '')):
          new_row['gross_unit_value'] = row[loaded_json['gross_unit_value']]
        else:
          if (loaded_json['gross_total_value'] is not '' and row[loaded_json['gross_total_value']] not in (None, '')):
            new_row['gross_unit_value'] = float(row[loaded_json['gross_total_value']]) / float(new_row["gross_unit_qty"])
          else:
            continue

        if (loaded_json['sku'] is not '' and row[loaded_json['sku']] not in (None, '')):
          new_row['sku'] = row[loaded_json['sku']]
        else:
          new_row['sku'] = ''

        if (loaded_json['product_id'] is not '' and row[loaded_json['product_id']] not in (None, '')):
          new_row['product_id'] = row[loaded_json['product_id']]
        else:
          new_row['product_id'] = ''

        writer.writerow(new_row)

if __name__ == "__main__":
  main()
