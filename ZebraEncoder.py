import huffmancodec
import Funcoes

def zebraEncoder():
    alfabeto8bit = list(range(0, 2 ** 8 + 1))
    zebraData = Funcoes.readFile("data/original/zebra.bmp")
    zebraData = Funcoes.turnDataIntoArray(zebraData, "bmp", alfabeto8bit)
    print("Original size: " + str(len(zebraData)))

    zebraData = Funcoes.turnToAsciiV2(zebraData)
    #

    zebraBlocks = Funcoes.breakIntoBlocks(100000, zebraData)
    stringBlock = []

    for block in zebraBlocks:
        stringBlock.append(Funcoes.listToString(block))


    #
    final = []
    for block in stringBlock:
        burrowWheeledAscii = Funcoes.bwt(block)
        rleEncoded = Funcoes.rleToList(Funcoes.rle_encode(burrowWheeledAscii))
        final += rleEncoded

    print("Size after RLE: " + str(len(final)))

    aux = huffmancodec.HuffmanCodec.from_data([1])
    final = final + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(final)
    encoded = codec.encode(final)
    print("done")
    print("Encoded size: " + str(len(encoded)))
    toWrite = {'t': codec.get_code_table(), 'd': encoded}
    Funcoes.write_file("encodedzebra.txt", toWrite)

def zebraDecoder(encodedData,table):
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
    blocks = Funcoes.breakIntoBlocks(100000, list(afterRLE))
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

if __name__ == "__main__":
    zebraEncoder()

    aux = Funcoes.read_file("encodedZebra.txt")

    table = aux['t']
    encodedData = aux['d']
    decompressedData = zebraDecoder(encodedData, table)