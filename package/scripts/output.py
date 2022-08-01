import os
import csv

def write_output_log(output_log, log_path):
    output_directory = 'htrvx_corrections'
    output_file_name = "output_"+str(os.path.basename(log_path.name)[:-4])+".csv"
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    with open(os.path.join(output_directory, output_file_name), 'w') as f:
        fieldnames = ["issue", "tag", "element", "file"]
        output_csv = csv.DictWriter(f, fieldnames=fieldnames)
        output_csv.writeheader()
        for line in output_log:
            output_csv.writerow({"issue":line.issue, "tag":line.tag, "element":line.element, "file":line.file,})