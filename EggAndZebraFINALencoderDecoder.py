import Funcoes
import huffmancodec
import numpy as np


def rleDeltaHuffmanGrouped(data, name):
    data = Funcoes.deltaFilter(data)

    toSum = np.array(data).min()

    data = Funcoes.sumExceptFirst(-toSum, data)
    data = Funcoes.turnToAsciiV2(data)

    data = Funcoes.rleToList(Funcoes.rle_encode(Funcoes.listToString(data)))
    aux = huffmancodec.HuffmanCodec.from_data([1])
    data = data + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(data)
    encoded = codec.encode(data)
    print("done")
    print("Encoded size: " + str(len(encoded)))
    toWrite = {'s': toSum, 't': codec.get_code_table(), 'd': encoded}
    Funcoes.write_file("data/encoded" + name + "G.txt", toWrite)
    return data


def decoder(name):
    encodedDict = Funcoes.read_file("data/encoded" + name + "G.txt")
    toSum = encodedDict['s']
    encodedData = encodedDict['d']
    codeTable = encodedDict['t']

    codec = huffmancodec.HuffmanCodec(codeTable)
    encodedData = codec.decode(encodedData)
    s = ""
    s = s.join(encodedData)
    encodedData = Funcoes.rle_decode(s)
    encodedData = Funcoes.turnAsciiToIntV2(encodedData)
    encodedData = Funcoes.sumExceptFirst(toSum, encodedData)
    encodedData = Funcoes.invDeltaFilter(encodedData)
    return encodedData


if __name__ == "__main__":
    data = Funcoes.readFile("data/original/zebra.bmp")
    data = Funcoes.turnDataIntoArray(data, "bmp", Funcoes.alfabeto8bit)
    copy = data.copy()
    rleDeltaHuffmanGrouped(data, "zebra")
    decoded = decoder("zebra")

    print(np.array(copy).sum() == np.array(decoded).sum())
