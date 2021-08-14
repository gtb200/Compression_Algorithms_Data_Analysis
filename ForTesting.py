import Final as f
import Funcoes
import numpy as np
import huffmancodec

def RleBwtDelta(data,name):
    data = Funcoes.deltaFilter(data)

    toSum = np.array(data).min()

    data = Funcoes.sumExceptFirst(-toSum, data)
    data = Funcoes.turnToAsciiV2(data)
    data = Funcoes.breakIntoBlocks(50000, data)
    stringBlock = []
    for block in data:
        stringBlock.append(Funcoes.listToString(block))
    final = []
    for block in stringBlock:
        burrowWheeledAscii = Funcoes.bwt(block)
        rleEncoded = Funcoes.rleToList(Funcoes.rle_encode(burrowWheeledAscii))
        final += rleEncoded

    print("RBD size: ",end="")
    print(len(Funcoes.listToString(final.copy())))
    return final

def RleBwt(data,name):


    data = Funcoes.turnToAsciiV2(data)
    data = Funcoes.breakIntoBlocks(50000, data)
    stringBlock = []
    for block in data:
        stringBlock.append(Funcoes.listToString(block))
    final = []
    for block in stringBlock:
        burrowWheeledAscii = Funcoes.bwt(block)
        rleEncoded = Funcoes.rleToList(Funcoes.rle_encode(burrowWheeledAscii))
        final += rleEncoded

    print("RB size: ",end="")
    print(len(Funcoes.listToString(final.copy())))
    return final
def rle(data,name):

    data = Funcoes.turnToAsciiV2(data)

    data = Funcoes.rleToList(Funcoes.rle_encode(Funcoes.listToString(data)))

    print("only rle size: ", end="")
    print(len(Funcoes.listToString(data.copy())))
    return data


def rleDelta(data, name):

    data = Funcoes.deltaFilter(data)

    toSum = np.array(data).min()

    data = Funcoes.sumExceptFirst(-toSum, data)
    data = Funcoes.turnToAsciiV2(data)


    data = Funcoes.rleToList(Funcoes.rle_encode(Funcoes.listToString(data)))

    print("rle with delta size: ", end="")
    print(len(Funcoes.listToString(data.copy())))
    return data

def rleDeltaHuffmanGrouped(data,name):

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
    toWrite = {'t': codec.get_code_table(), 'd': encoded}
    Funcoes.write_file("data/encoded"+name+"G.txt", toWrite)
    return data
def rleDeltaHuffmanNOTGrouped(data,name):

    data = Funcoes.deltaFilter(data)

    toSum = np.array(data).min()

    data = Funcoes.sumExceptFirst(-toSum, data)
    data = Funcoes.turnToAsciiV2(data)


    data = Funcoes.rleToListV2(Funcoes.rle_encode(Funcoes.listToString(data)))
    aux = huffmancodec.HuffmanCodec.from_data([1])
    data = data + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(data)
    encoded = codec.encode(data)
    print("done")
    print("Encoded size: " + str(len(encoded)))
    toWrite = {'t': codec.get_code_table(), 'd': encoded}
    Funcoes.write_file("data/encoded"+name+"NG.txt", toWrite)
    return data
def rleHuffmanNOTGrouped(data,name):



    data = Funcoes.turnToAsciiV2(data)


    data = Funcoes.rleToListV2(Funcoes.rle_encode(Funcoes.listToString(data)))
    aux = huffmancodec.HuffmanCodec.from_data([1])
    data = data + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(data)
    encoded = codec.encode(data)
    print("done")
    print("Encoded size: " + str(len(encoded)))
    toWrite = {'t': codec.get_code_table(), 'd': encoded}
    Funcoes.write_file("data/encoded"+name+"NG.txt", toWrite)
    return data
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
def justHuffman(data,name):
    aux = huffmancodec.HuffmanCodec.from_data([1])
    data = list(data) + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(data)
    encoded = codec.encode(data)
    print("done")
    print("Encoded size: " + str(len(encoded)))
    toWrite = {'t': codec.get_code_table(), 'd': encoded}
    Funcoes.write_file("data/encoded"+name+"justHuffman.txt", toWrite)
    return data
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
def main():
    alfabeto8bitDelta = list(range(-(2 ** 8 + 1), 2 ** 8 + 1))  # Este é usado nos ficheiros bmp e wav [0 ... 255]

    names = ["zebra.bmp","landscape.bmp","egg.bmp","pattern.bmp"]

    for name in names:

        data = Funcoes.readFile("data/original/"+name)
        data = Funcoes.turnDataIntoArray(data,"bmp",f.alfabeto8bit)
        print("Original size " + name + ": " + str(len(data)))

        deltaHuffman(data,name)

        # rleBwtDelta = RleBwtDelta(data.copy(),name)
        # contagem,alfabeto = f.contagemNova(list(rleBwtDelta),"bmp")
        # print("RBD entropia g: "+ str(f.entropia(contagem)))
        # print("size: ",end="")
        # print(len(rleBwtDelta))
        # contagem,alfabeto = f.contagemNova(Funcoes.rleToListV2(Funcoes.listToString(list(rleBwtDelta))),"bmp")
        #
        # print("RBD entropia not g: "+ str(f.entropia(contagem)))
        # print("size: ",end="")
        # print(len(Funcoes.rleToListV2(Funcoes.listToString(list(rleBwtDelta)))))
        #
        # rb = RleBwt(data.copy(),name)
        # contagem,alfabeto = f.contagemNova(list(rb),"bmp")
        # print("RB entropia g: "+ str(f.entropia(contagem)))
        # print("size: ",end="")
        # print(len(rb))
        # contagem,alfabeto = f.contagemNova(Funcoes.rleToListV2(Funcoes.listToString(list(rb))),"bmp")
        # print("RB entropia not g: "+ str(f.entropia(contagem)))
        # print("size: ",end="")
        # print(len(Funcoes.rleToListV2(Funcoes.listToString(list(rb)))))
        #
        #
        # onlyRle = rle(data.copy(),name)
        # contagem, alfabeto = f.contagemNova(list(onlyRle), "bmp")
        # print("Rle only entropia g: " + str(f.entropia(contagem)))
        # print("size: ",end="")
        # print(len(onlyRle))
        # contagem, alfabeto = f.contagemNova(Funcoes.rleToListV2(Funcoes.listToString(list(onlyRle))), "bmp")
        # print("Rle only entropia not g: " + str(f.entropia(contagem)))
        # print("size: ",end="")
        # print(len(Funcoes.rleToListV2(Funcoes.listToString(list(onlyRle)))))
        #
        #
        # rleWithDelta = rleDelta(data.copy(),name)
        # contagem, alfabeto = f.contagemNova(list(rleWithDelta), "bmp")
        # print("Rle with delta entropia g: " + str(f.entropia(contagem)))
        # print("size: ",end="")
        # print(len(rleWithDelta))
        # contagem, alfabeto = f.contagemNova(Funcoes.rleToListV2(Funcoes.listToString(list(rleWithDelta))), "bmp")
        # print("Rle with delta entropia not g: " + str(f.entropia(contagem)))
        # print("size: ",end="")
        # print(len(Funcoes.rleToListV2(Funcoes.listToString(list(rleWithDelta)))))


        #contagem , alfabeto = f.contagemNova(data,"bmp",alfabeto8bitDelta)
        #print(name +": "+str(f.entropia(contagem)))

        #f.histograma(contagem,alfabeto)

if __name__ == "__main__":
    main()