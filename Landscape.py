import Funcoes
import huffmancodec
import numpy as np


def encodeMain(filename):
    alfabeto8bit = list(range(0, 2 ** 8 + 1))  # Este é usado nos ficheiros bmp e wav [0 ... 255]
    dataLandscape = Funcoes.readFile(filename)
    dataLandscape = Funcoes.turnDataIntoArray(dataLandscape, "bmp", alfabeto8bit)
    print("Inicial size: " + str(len(dataLandscape)))
    print("Starting delta filter encoding")
    deltaLandscape = Funcoes.deltaFilter(dataLandscape)
    deltaLandscape67 = Funcoes.sumExceptFirst(67, deltaLandscape)
    print("Done")
    print("Turning Values to Ascii")
    deltaLandscapeAscii67 = Funcoes.turnToAscii(deltaLandscape67)
    print("Breaking source into blocks")
    blockAscii = Funcoes.breakIntoBlocks(100000, deltaLandscapeAscii67)
    stringBlock = []
    for block in blockAscii:
        stringBlock.append(Funcoes.listToString(block))
    final = []
    print("Starting Burrow Wheeler transform and rle on each block")
    for block in stringBlock:
        burrowWheeledAscii = Funcoes.bwt(block)
        rleEncoded = Funcoes.rleToList(Funcoes.rle_encode(burrowWheeledAscii))
        final += rleEncoded
    print("done")
    print("Starting huffman encoding")
    aux = huffmancodec.HuffmanCodec.from_data([1])
    final = final + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(final)
    encoded = codec.encode(final)
    print("done")
    print("Encoded size: " + str(len(encoded)))
    return encoded, codec.get_code_table(), codec.get_code_len()


def decode(encodedData, table):
    print("Decoding huffman")
    codec = huffmancodec.HuffmanCodec(table)
    afterHuffman = codec.decode(encodedData)
    print("Done")
    s = ""
    s = s.join(afterHuffman)
    print("Start decoding rle")
    afterRLE = Funcoes.rle_decode(s)
    print("end decoding rle")
    print("Breaking into blocks")
    blocks = Funcoes.breakIntoBlocks(100000, list(afterRLE))
    print("Done")
    final = []
    i = 0

    for block in blocks:
        if i % 1000 == 0:
            print("Invert Burrow Wheeler progress: " + str((i * 100) / 100000) + "%")
        x = ""
        x = x.join(block)

        final += list(Funcoes.ibwt(block))
        i += 1
    print("Done")
    print("Reverting Ascii and reverting delta filter")
    data = Funcoes.turnAsciiToInt(final)
    data = Funcoes.sumExceptFirst(-67, data)
    data = Funcoes.invDeltaFilter(data)
    print("Final decoded size: " + str(len(data)))
    return data


if __name__ == "__main__":
    encode = 1
    decoder = 1

    if encode == 1 :
        alfabeto8bit = list(range(0, 2 ** 8 + 1))

        encoded, t, l = encodeMain("data/original/Landscape.bmp")
        toWrite = {'t': t, 'd': encoded}
        print("Encoded size (including code table): " + str(len(t) + len(encoded)))
        Funcoes.write_file("encodedLandscape.txt", toWrite)

    if decoder == 1:
        _encoded = Funcoes.read_file("encodedLandscape.txt")
        dataEncoded = _encoded['d']
        table = _encoded['t']
        decoded = decode(dataEncoded, table)

        dataLandscape = Funcoes.readFile("data/original/Landscape.bmp")
        dataLandscape = Funcoes.turnDataIntoArray(dataLandscape, "bmp", alfabeto8bit)
        print("Checksuming")
        print(np.array(decoded).sum() == np.array(dataLandscape).sum())
