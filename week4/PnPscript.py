# Pick and Place Machine Conversion Script for Regulator PCB
# EEL3926 Junior Design
# March 3th, 2025
# Author: Binh Pham
# Template file was modified from example file provided by NeoDen YY1 Manufacturer
# https://neodenusa.com/neoden-yy1-pick-place-machine/
# Disclaimer: The use of the program is for educational purpose only and not for 
# commercial use

#----------------------------------------------------------------------------------

import csv #CSV (Comma Seperated Values) Library

#----------------------------------------------------------------------------------
# Declare file names
#----------------------------------------------------------------------------------
# Input from students, generated from Fusion's pick and place file
# Note: File need to be modified with correct ordering in the last column
# MSP430: 1; Capacitors: 2, 3; Inductor: 4; LED: 5; Resistor: 6 
inputFile = "PnP_Junior_Reg_front.csv"
# Template modified from NeoDen YY1 example
# Setting are specific to EEL3926's regulators PCB
template = "Template.csv"
# Rearraged file with correct order and added header
o_inputFile = "Ordered_inputFile.csv"
# Seperate file with student name as output
outputFile = "StudentOutputFile.csv"

#----------------------------------------------------------------------------------
# Open, read input file and rearrange in correct order

# Open and covert each row in to list
with open(inputFile, "r", newline='') as inFile:
    inFile_reader = csv.reader(inFile)
    inFile_line = list(inFile_reader)
    # print(line)
for line in (inFile_line):
	if line[6] == "":
		inFile_line.remove(line)

# Sort row based on the last column index
# key = lambda, anonymous callable function to create inline function without define
# This point the list of elements then sorted them
# for x[-1] point to the last column
inFile_line.sort(key=lambda x: int(x[-1]))
#print(line)

# Write sorted data into a separate file and add header
with open(o_inputFile, "w", newline='') as orderedFile:
    ordered_writer = csv.writer(orderedFile)
    # Write header to matched with header existed in template
    ordered_writer.writerow(["Designator", "Mid X(mm)", "Mid Y(mm) ", "Rotation", "Comment", "Footprint", "FeederNo"])
    # Write sorted line to new file
    ordered_writer.writerows(inFile_line)

# Read back in the new ordered file
with open(o_inputFile, "r", newline ='') as sFile:
    sFile_reader = csv.DictReader(sFile)
    s_lines = list(sFile_reader)

# Read in template to extract headers
with open(template, "r", newline='') as oFile:
    oFile_reader = csv.reader(oFile)
    o_reader = list(oFile_reader)

# Template file have header at line 12, file change start at 11
h_index = 11

# Read in header start from line 11 and then indexing each header base on column location
header = o_reader[h_index]

indexingHeader = {col: i for i, col in enumerate(header)}

# Set output data line after the header line
o_data = o_reader[h_index + 1:]

# Change items in each line of the output file to the correct items in the ordered input
for i, o_line in enumerate(o_data):
    # Create constraint to check for the number of lines
    if i<len(s_lines):
        src_line = s_lines[i]
        # Check if elements existed in the template, and if empty input items from ordered input
        for col, s_data in src_line.items():
            if col in indexingHeader:
                # Change index
                idx = indexingHeader[col]
                # Only input when the element is empty
                if o_line[idx] == "":
                    o_line[idx] = s_data
    # Switch to next line
    o_data[i] = o_line

# Write data to out put file
with open(outputFile, "w", newline='') as outFile:
    outFile_writer = csv.writer(outFile)
    # Write existing information from the first 11 line
    for line in o_reader[:h_index]:
        outFile_writer.writerow(line)
    # Write headers
    outFile_writer.writerow(header)
    # Write new data
    for line in o_data:
        outFile_writer.writerow(line)
print("Updated CSV written to", outputFile)