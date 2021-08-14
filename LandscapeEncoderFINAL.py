import Funcoes
import huffmancodec
import numpy as np

def deltaHuffman(data,name):
    data = Funcoes.deltaFilter(data)
    aux = huffmancodec.HuffmanCodec.from_data([1])
    data = list(data) + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(data)
    encoded = codec.encode(data)
    print("done")
    print("Encoded size: " + str(len(encoded)))
    toWrite = {'t': codec.get_code_table(), 'd': encoded}
    Funcoes.write_file("data/encoded" + name + "deltaHuffman.txt", toWrite)
    return data

def decoder(name):
    encodedDict = Funcoes.read_file("data/encoded" + name + "deltaHuffman.txt")
    encodedData = encodedDict['d']
    codeTable = encodedDict['t']

    codec = huffmancodec.HuffmanCodec(codeTable)
    encodedData = list(codec.decode(encodedData))
    encodedData = Funcoes.invDeltaFilter(encodedData)
    return encodedData

if __name__ == "__main__":
    data = Funcoes.readFile("data/original/landscape.bmp")
    data = Funcoes.turnDataIntoArray(data, "bmp", Funcoes.alfabeto8bit)

    deltaHuffman(data,"Landscape")

    decoded = decoder("Landscape")

    print(np.array(data).sum() == np.array(decoded).sum())
