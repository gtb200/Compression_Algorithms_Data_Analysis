#
# Compression application using static arithmetic coding
#
# Usage: python arithmetic-compress.py InputFile OutputFile
# Then use the corresponding arithmetic-decompress.py application to recreate the original input file.
# Note that the application uses an alphabet of 257 symbols - 256 symbols for the byte
# values and 1 symbol for the EOF marker. The compressed file format starts with a list
# of 256 symbol frequencies, and then followed by the arithmetic-coded data.
#
# Copyright (c) Project Nayuki
#
# https://www.nayuki.io/page/reference-arithmetic-coding
# https://github.com/nayuki/Reference-arithmetic-coding
#

import Funcoes
import huffmancodec
import numpy as np

def eggEncoder():
    alfabeto8bit = list(range(0, 2 ** 8 + 1))
    eggData = Funcoes.readFile("data/original/egg.bmp")
    eggData = Funcoes.turnDataIntoArray(eggData,"bmp",alfabeto8bit)
    print("Original size: "+str(len(eggData)))

    eggData = Funcoes.turnToAsciiV2(eggData)
#

    eggBlocks=Funcoes.breakIntoBlocks(105519,eggData)
    stringBlock=[]

    for block in eggBlocks:
        stringBlock.append(Funcoes.listToString(block))

    #eggData = Funcoes.listToString(eggData)
    #eggData = Funcoes.rle_encode(eggData)

#
    final=[]
    for block in stringBlock:
        burrowWheeledAscii = Funcoes.bwt(block)
        rleEncoded = Funcoes.rleToList(Funcoes.rle_encode(burrowWheeledAscii))
        final += rleEncoded

    print("Size after RLE: "+str(len(final)))
    #Funcoes.write_file("data/eggAuxCompressed.data",final)     Usar estes dois se quiser usar aritmetica
    #Funcoes.main(["data/eggAuxCompressed.data","eggCompressed.data"])   env

    aux = huffmancodec.HuffmanCodec.from_data([1])
    final = final + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(final)
    encoded = codec.encode(final)
    print("done")
    print("Encoded size: " + str(len(encoded)))
    toWrite = {'t': codec.get_code_table(), 'd': encoded}
    Funcoes.write_file("encodedEgg.txt", toWrite)

    #print("Final size: "+str(len(Funcoes.read_fileNoPickle("eggCompressed.data"))))

def eggDecoder(encodedData,table):
    print("Decoding huffman")
    codec = huffmancodec.HuffmanCodec(table)
    afterHuffman = codec.decode(encodedData)
    print("Done")
    s = ""
    s = s.join(afterHuffman)
    print("Start decoding rle")
    afterRLE = Funcoes.rle_decode(s)
    print(len(list(afterRLE)))
    print("end decoding rle")
    print("Breaking into blocks")
    blocks = Funcoes.breakIntoBlocks(105519, list(afterRLE))
    print("Done")
    final = []
    i = 0
    print(len(blocks[-1]))

    for block in blocks:
        if i % 1000 == 0:
            print("Invert Burrow Wheeler progress: " + str((i * 100) / 100000) + "%")
        x = ""
        x = x.join(block)

        final += list(Funcoes.ibwt(block))
        i += 1
    print("Done")
    print("Reverting Ascii and reverting delta filter")
    data = Funcoes.turnAsciiToIntV2(final)
    print("Final decoded size: " + str(len(data)))
    return data
# Main launcher
if __name__ == "__main__":
    eggEncoder()

    aux = Funcoes.read_file("encodedEgg.txt")

    table= aux['t']
    encodedData= aux['d']
    decompressedData=eggDecoder(encodedData,table)