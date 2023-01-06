import sys
import os


def write_instructions(file_name, instruction_list):
    # Convert file extension
    file_name = file_name.replace(".asm", ".hack")
    # Open file and clear previous data
    outfile = open(file_name, "a+")
    outfile.truncate(0)
    # Write all instructions to outfile
    for instruction in instruction_list:
        print(instruction)
        outfile.write(instruction + "\n")
    outfile.close()


def parse_a(line):
    # Convert a string representation of an int to a binary representation
    number = line.split("@")[1]
    int_instruction = int(number)
    bin_instruction = "{:016b}".format(int_instruction)
    return bin_instruction


def get_destination(destination):
    # Returns the correct destination bits for the specified destination
    dest_bits = []
    dest_bits.append("1") if "A" in destination else dest_bits.append("0")
    dest_bits.append("1") if "D" in destination else dest_bits.append("0")
    dest_bits.append("1") if "M" in destination else dest_bits.append("0")
    return dest_bits


def get_computation(computation):
    comp_bits = []

    # Set comparison bit 1
    comp_bits.append("1") if "M" in computation else comp_bits.append("0")

    # Set comparison bits 2-7
    if computation == "0":
        comp_bits.append("101010")
    elif computation == "1":
        comp_bits.append("111111")
    elif computation == "-1":
        comp_bits.append("111010")
    elif computation == "D":
        comp_bits.append("001100")
    elif computation == "A" or computation == "M":
        comp_bits.append("110000")
    elif computation == "!D":
        comp_bits.append("001101")
    elif computation == "!A" or computation == "!M":
        comp_bits.append("110001")
    elif computation == "-D":
        comp_bits.append("001111")
    elif computation == "-A" or computation == "-M":
        comp_bits.append("110011")
    elif computation == "D+1":
        comp_bits.append("011111")
    elif computation == "A+1" or computation == "M+1":
        comp_bits.append("110111")
    elif computation == "D-1":
        comp_bits.append("001110")
    elif computation == "A-1" or computation == "M-1":
        comp_bits.append("110010")
    elif computation == "D+A" or computation == "D+M":
        comp_bits.append("000010")
    elif computation == "D-A" or computation == "D-M":
        comp_bits.append("010011")
    elif computation == "A-D" or computation == "M-D":
        comp_bits.append("000111")
    elif computation == "D&A" or computation == "D&M":
        comp_bits.append("000000")
    elif computation == "D|A" or computation == "D|M":
        comp_bits.append("010101")
    return comp_bits


def get_jump(jump):
    # Returns corresponding bits for the specified jump command
    if jump == "JGT":
        return "001"
    elif jump == "JEQ":
        return "010"
    elif jump == "JGE":
        return "011"
    elif jump == "JLT":
        return "100"
    elif jump == "JNE":
        return "101"
    elif jump == "JLE":
        return "110"
    elif jump == "JMP":
        return "111"


def parse_line(line):
    # Ignore commented lines
    if len(line) > 1 and line[0] == "/" and line[1] == "/":
        return

    # Remove any in-line comments, and parse white space
    if "//" in line:
        split_line = line.split("//")
        line = split_line[0]
    line = line.strip()

    # Ignore blank lines
    if not line:
        return

    # Handle A instructions
    if line[0] == "@":
        return parse_a(line)

    # Handle C instructions
    computation_bits = None
    # Means we will have a destination and computation
    if "=" in line:
        split_line = line.split("=")
        destination = split_line[0]
        dest_bits = get_destination(destination)

        computation = split_line[1]
        computation_bits = get_computation(computation)
    # Default values when no destination present in command
    else:
        dest_bits = ["0","0","0"]

    # Means we will have a jump and computation
    if ";" in line:
        split_line = line.split(";")
        if not computation_bits:
            computation = split_line[0]
            computation_bits = get_computation(computation)
        jump = split_line[1]
        jump_bits = get_jump(jump)
    # Default value when no jump present in command
    else:
        jump_bits = "000"

    # Computation is required for a valid command
    if not computation_bits:
        return

    # Parse op code 111 with computation, destination, and jump bits
    final_instruction = "111" + ''.join(computation_bits) + ''.join(dest_bits) + jump_bits
    return final_instruction


def generate_instructions(file_name):
    instruction_list = []
    with open(file_name) as infile:
        for line in infile:
            instruction = parse_line(line)
            if instruction:
                instruction_list.append(instruction)
    return instruction_list


def main():
    # Get file from command line
    try:
        file_name = sys.argv[1]
    except IndexError:
        print("usage: assembler.py input_file")
        exit()
    # Ensure file exists
    if not os.path.exists(file_name):
        print("File", file_name, "not found!")
        exit()

    #populate_labels(file_name)
    instruction_list = generate_instructions(file_name)
    write_instructions(file_name, instruction_list)


main()
