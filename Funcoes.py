import numpy as np
import pickle
import matplotlib.image as mpimg
import arithmeticcoding
import contextlib, sys

alfabeto8bit = list(range(0, 2 ** 8 + 1))  # Este é usado nos ficheiros bmp e wav [0 ... 255]


def readFile(filename):

    if (filename[len(filename) - 3:] == "bmp"):
        data = mpimg.imread(filename)
        return data


def turnDataIntoArray(data, type, alfabeto):
    resultado = []
    if (type == "bmp"):
        if (len(data.shape) == 3):
            for linha in data:
                resultado.append(linha[:, 0])
            return np.array(resultado).flatten()
        else:
            return data.flatten()


def deltaFilter(data):
    resultado = np.zeros(len(data), dtype=int)
    for index in range(len(data)):
        if index == 0:
            resultado[index] = data[index]
        else:
            resultado[index] = int(data[index]) - int(data[index - 1])

    return resultado


def invDeltaFilter(data):
    for index in range(len(data)):
        if index == 0:
            continue
        else:
            data[index] = int(data[index]) + int(data[index - 1])
    return data


def sumExceptFirst(value, array):
    for i in range(1, len(array)):
        array[i] += value

    return array


def turnToAscii(array):
    resultado = []
    for i in range(len(array)):
        charToAdd = chr(array[i])
        if charToAdd == "\002":
            charToAdd = chr(200)
        elif charToAdd == "\003":
            charToAdd = chr(201)
        elif charToAdd in "0123456789":
            charToAdd = chr(int(charToAdd) + 202)
        resultado.append(charToAdd)

    return resultado

def turnToAsciiV2(array):
    resultado = []
    for i in range(len(array)):
        charToAdd = chr(array[i])
        if charToAdd == "\002":
            charToAdd = chr(800)
        elif charToAdd == "\003":
            charToAdd = chr(801)
        elif charToAdd in "0123456789":
            charToAdd = chr(int(charToAdd) + 802)
        resultado.append(charToAdd)

    return resultado
def breakIntoBlocks(howMany, array):
    blockSize = len(array) // howMany
    left = len(array) % howMany
    index = 0
    resultado = []
    while index < blockSize * howMany:
        resultado.append(array[index:(index + blockSize)])
        index += blockSize
    if left > 0:
        resultado[-1] += array[index:]
    return resultado


def listToString(array):
    s = ""
    return s.join(array)


def bwt(s):
    """Apply Burrows-Wheeler transform to input string."""
    assert "\002" not in s and "\003" not in s, "Input string cannot contain STX and ETX characters"
    s = "\002" + s + "\003"  # Add start and end of text marker
    table = sorted(s[i:] + s[:i] for i in range(len(s)))  # Table of rotations of string
    last_column = [row[-1:] for row in table]  # Last characters of each row
    return "".join(last_column)  # Convert list of characters into string


def rle_encode(data):
    encoding = ''
    prev_char = ''
    count = 1

    if not data: return ''

    for char in data:
        # If the prev and current characters
        # don't match...
        if char != prev_char:
            # ...then add the count and character
            # to our encoding
            if prev_char:
                encoding += str(count) + prev_char
            count = 1
            prev_char = char
        else:
            # Or increment our counter
            # if the characters do match
            count += 1
    else:
        # Finish off the encoding
        encoding += str(count) + prev_char
        return encoding


def rleToList(string):
    resultado = []
    toAdd = ""
    for i in string:
        if i.isdigit() and i not in  "¹°²³":
            toAdd += i
        else:
            toAdd += i
            resultado.append(toAdd)
            toAdd = ""
    # for i in range(0, len(string), 2):
    #    resultado.append(string[i:i + 2])
    return resultado

def rleToListV2(string):
    resultado = []
    toAdd = ""
    for i in string:
        if i.isdigit() and i not in  "¹°²³":
            toAdd += i
        else:
            if toAdd != "":
                resultado.append(toAdd)
                toAdd = ""
            toAdd += i
            resultado.append(toAdd)
            toAdd = ""
    # for i in range(0, len(string), 2):
    #    resultado.append(string[i:i + 2])
    return resultado

def write_file(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
        f.close()


def ibwt(r):
    """Apply inverse Burrows-Wheeler transform."""
    table = [""] * len(r)  # Make empty table
    for i in range(len(r)):
        table = sorted(r[i] + table[i] for i in range(len(r)))  # Add a column of r
    s = [row for row in table if row.endswith("\003")][0]  # Find the correct row (ending in ETX)
    return s.rstrip("\003").strip("\002")  # Get rid of start and end markers


def read_file(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        f.close()
        return data


def rle_decode(data):
    decode = ''
    count = ''
    for char in data:
        # If the character is numerical...
        if char.isdigit() and char not in "¹°²³":
            # ...append it to our count
            count += char
        else:
            # Otherwise we've seen a non-numerical
            # character and need to expand it for
            # the decoding
            decode += char * int(count)
            count = ''
    return decode


def turnAsciiToInt(string):
    final = []
    comp = chr(200) + chr(201) + chr(202) + chr(203) + chr(204) + chr(205) + chr(206) + chr(207) + chr(208) + chr(
        209) + chr(210) + chr(211)
    for char in string:
        if char in comp:
            if comp.index(char) >= 2:
                final.append(48 + comp.index(char) - 2)
            else:
                final.append(2 + comp.index(char))
        else:
            final.append(ord(char))
    return final

def turnAsciiToIntV2(string):
    final = []
    comp = chr(800) + chr(801)+ chr(802) + chr(803) + chr(804) + chr(805) + chr(806) + chr(807) + chr(808) + chr(
        809) + chr(810) + chr(811)
    for char in string:
        if char in comp:
            if comp.index(char) >= 2:
                final.append(48 + comp.index(char) - 2)
            else:
                final.append(2 + comp.index(char))
        else:
            final.append(ord(char))
    return final

# Command line main application function.
def main(args):
    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: python arithmetic-compress.py InputFile OutputFile")
    inputfile, outputfile = args

    # Read input file once to compute symbol frequencies
    freqs = get_frequencies(inputfile)
    freqs.increment(256)  # EOF symbol gets a frequency of 1

    # Read input file again, compress with arithmetic coding, and write output file
    with open(inputfile, "rb") as inp, \
            contextlib.closing(arithmeticcoding.BitOutputStream(open(outputfile, "wb"))) as bitout:
        write_frequencies(bitout, freqs)
        compress(freqs, inp, bitout)


# Returns a frequency table based on the bytes in the given file.
# Also contains an extra entry for symbol 256, whose frequency is set to 0.
def get_frequencies(filepath):
    freqs = arithmeticcoding.SimpleFrequencyTable([0] * 257)
    with open(filepath, "rb") as input:
        while True:
            b = input.read(1)
            if len(b) == 0:
                break
            freqs.increment(b[0])
    return freqs


def write_frequencies(bitout, freqs):
    for i in range(256):
        write_int(bitout, 32, freqs.get(i))


def compress(freqs, inp, bitout):
    enc = arithmeticcoding.ArithmeticEncoder(32, bitout)
    while True:
        symbol = inp.read(1)
        if len(symbol) == 0:
            break
        enc.write(freqs, symbol[0])
    enc.write(freqs, 256)  # EOF
    enc.finish()  # Flush remaining code bits


# Writes an unsigned integer of the given bit width to the given stream.
def write_int(bitout, numbits, value):
    for i in reversed(range(numbits)):
        bitout.write((value >> i) & 1)  # Big endian

def read_fileNoPickle(filename):
    with open(filename, 'rb') as f:
        data=f.read()
        f.close()
        return data

def readFile(filename):

    if (filename[len(filename) - 3:] == "bmp"):
        data = mpimg.imread(filename)
        return data


def turnDataIntoArray(data, type, alfabeto):
    resultado = []
    if (type == "bmp"):
        if (len(data.shape) == 3):
            for linha in data:
                resultado.append(linha[:, 0])
            return np.array(resultado).flatten()
        else:
            return data.flatten()

