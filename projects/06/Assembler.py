import sys
import os

# Symbol table holds predefined symbols, and user specified symbols are populated on first pass
symbol_table = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SCREEN": "16384",
    "KBD": "24576",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4"
}
# Hack language specification dictates address 16 is the first viable storage location
symbol_loc = 16


def write_instructions(file_name, instruction_list):
    """
    Write all instructions to the output file
    :param file_name: File name to which output will be written
    :param instruction_list: List containing 16 character representations of each instruction
    :return: None
    """
    # Convert file extension
    file_name = file_name.replace(".asm", ".hack")
    # Open file and clear previous data
    outfile = open(file_name, "a+")
    outfile.truncate(0)
    # Write all instructions to outfile
    for instruction in instruction_list:
        outfile.write(instruction + "\n")
    outfile.close()


def parse_a(line):
    """
    Convert an A instruction into a 16 character string of 1's and 0's representing the given instruction
    :param line: A line containing an A instruction
    :return: 16 character string of 1's and 0's representing the given instruction
    """
    number = line.split("@")[1]
    # Attempt to convert A instruction into an int
    try:
        int_instruction = int(number)
    # Instruction is a symbol
    except ValueError:
        global symbol_loc
        # If symbol already in the table, lookup the value
        if number in symbol_table:
            int_instruction = int(symbol_table[number])
        # If symbol not in table, add the value to the table
        else:
            int_instruction = int(symbol_loc)
            symbol_table[number] = symbol_loc
            symbol_loc += 1
    # Convert int to string representation of 1's and 0's
    finally:
        bin_instruction = "{:016b}".format(int_instruction)
        return bin_instruction


def get_destination(destination):
    """
    Returns the correct destination bits for the specified destination
    :param destination: A string containing the destination of a C instruction
    :return: String representing the three destination bits
    """
    dest_bits = ""
    if "A" in destination:
        dest_bits += "1"
    else:
        dest_bits += "0"
    if "D" in destination:
        dest_bits += "1"
    else:
        dest_bits += "0"
    if "M" in destination:
        dest_bits += "1"
    else:
        dest_bits += "0"
    return dest_bits


def get_computation(computation):
    """
    Returns the correct computation bits for the specified destination
    :param computation: A string containing the computation of a C instruction
    :return: String representing the three computation bits
    """
    comp_bits = ""

    # Set comparison bit 1
    if "M" in computation:
        comp_bits += "1"
    else:
        comp_bits += "0"

    # Set comparison bits 2-7
    if computation == "0":
        comp_bits += "101010"
    elif computation == "1":
        comp_bits += "111111"
    elif computation == "-1":
        comp_bits += "111010"
    elif computation == "D":
        comp_bits += "001100"
    elif computation == "A" or computation == "M":
        comp_bits += "110000"
    elif computation == "!D":
        comp_bits += "001101"
    elif computation == "!A" or computation == "!M":
        comp_bits += "110001"
    elif computation == "-D":
        comp_bits += "001111"
    elif computation == "-A" or computation == "-M":
        comp_bits += "110011"
    elif computation == "D+1":
        comp_bits += "011111"
    elif computation == "A+1" or computation == "M+1":
        comp_bits += "110111"
    elif computation == "D-1":
        comp_bits += "001110"
    elif computation == "A-1" or computation == "M-1":
        comp_bits += "110010"
    elif computation == "D+A" or computation == "D+M":
        comp_bits += "000010"
    elif computation == "D-A" or computation == "D-M":
        comp_bits += "010011"
    elif computation == "A-D" or computation == "M-D":
        comp_bits += "000111"
    elif computation == "D&A" or computation == "D&M":
        comp_bits += "000000"
    elif computation == "D|A" or computation == "D|M":
        comp_bits += "010101"
    return comp_bits


def get_jump(jump):
    """
    Returns the correct jump bits for the specified instruction
    :param jump: A string containing the jump of a C instruction
    :return: String representing the three jump bits
    """
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
    """
    Checks a line for a valid instruction. If present, converts the instruction into a
    16 character string of 1's and 0's representing the given instruction
    :param line: The line to parse
    :return: Returns a 16 character string of 1's and 0's representing the given instruction if present; else None
    """
    # Validate the line
    line = check_line(line)

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
        # Handle destination
        split_line = line.split("=")
        destination = split_line[0]
        dest_bits = get_destination(destination)
        # Handle computation
        computation = split_line[1]
        computation_bits = get_computation(computation)
    # Default values when no destination present in command
    else:
        dest_bits = "000"

    # Means we will have a jump and computation
    if ";" in line:
        # Handle computation if not already handled
        split_line = line.split(";")
        if not computation_bits:
            computation = split_line[0]
            computation_bits = get_computation(computation)
        # Handle jump
        jump = split_line[1]
        jump_bits = get_jump(jump)
    # Default value when no jump present in command
    else:
        jump_bits = "000"

    # Computation is required for a valid command
    if not computation_bits:
        return

    # Parse op code 111 with computation, destination, and jump bits
    final_instruction = "111" + computation_bits + dest_bits + jump_bits
    return final_instruction


def generate_instructions(file_name):
    """
    Opens a file, and sends each line for parsing
    :param file_name: Valid .asm file to read instructions from
    :return: List containing 16 character representations of each instruction
    """
    instruction_list = []
    with open(file_name) as infile:
        for line in infile:
            instruction = parse_line(line)
            # Lines without instructions are not added for writing
            if instruction:
                instruction_list.append(instruction)
    return instruction_list


def check_line(line):
    """
    Validates lines before parsing
    :param line: Line to validate
    :return: The line with comments and white space removed
    """
    # Ignore commented lines
    if len(line) > 1 and line[0] == "/" and line[1] == "/":
        return

    # Remove any in-line comments, and parse white space
    if "//" in line:
        split_line = line.split("//")
        line = split_line[0]
    line = line.strip()

    return line


def populate_labels(file_name):
    """
    First pass to populate labels within the symbol table
    :param file_name: Valid .asm file to read instructions from
    :return: None
    """
    # Keeps track of the current instruction line
    line_count = 0
    with open(file_name) as infile:
        for line in infile:
            # Validate each line
            line = check_line(line)
            if line:
                # If a label is present, add the label to the symbol table
                if line[0] == "(":
                    label = line[line.find("(")+1:line.rfind(")")]
                    symbol_table[label] = line_count
                # Increment to notate the next instruction line
                else:
                    line_count += 1


def main():
    """
    Driver for the assembler. Validates the file is valid before calling other methods.
    :return: None
    """
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

    populate_labels(file_name)
    instruction_list = generate_instructions(file_name)
    write_instructions(file_name, instruction_list)


main()
