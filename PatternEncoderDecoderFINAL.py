import huffmancodec
import numpy as np
import Funcoes


def rleHuffmanGrouped(data,name):



    data = Funcoes.turnToAsciiV2(data)


    data = Funcoes.rleToList(Funcoes.rle_encode(Funcoes.listToString(data)))
    aux = huffmancodec.HuffmanCodec.from_data([1])
    data = data + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(data)
    encoded = codec.encode(data)
    print("done")
    print("Encoded size: " + str(len(encoded)))
    toWrite = {'t': codec.get_code_table(), 'd': encoded}
    Funcoes.write_file("data/encoded"+name+"G.txt", toWrite)
    return data

def decoder(name):
    encodedDict = Funcoes.read_file("data/encoded" + name + "G.txt")
    encodedData = encodedDict['d']
    codeTable = encodedDict['t']

    codec = huffmancodec.HuffmanCodec(codeTable)
    encodedData = codec.decode(encodedData)
    s = ""
    s = s.join(encodedData)
    encodedData = Funcoes.rle_decode(s)
    encodedData = Funcoes.turnAsciiToIntV2(encodedData)

    return encodedData

if __name__ == "__main__":
    data = Funcoes.readFile("data/original/Pattern.bmp")
    data = Funcoes.turnDataIntoArray(data, "bmp", Funcoes.alfabeto8bit)

    rleHuffmanGrouped(data,"Pattern")

    decoded = decoder("Pattern")

    print(np.array(data).sum() == np.array(decoded).sum())
