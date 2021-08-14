import pickle
import huffmancodec



def convertListofListsToListofStrings(input):
    resultado = []
    fonte=input.copy()
    for array in fonte:
        resultado.append(str(array[0])+","+str(array[1])+","+str(array[2]))
    return resultado

def write_file(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
        f.close()



def encode():
    with open('teste.data', 'rb') as filehandle:
        # read the data as binary data stream
        encodedData = pickle.load(filehandle)

    encodedData=convertListofListsToListofStrings(encodedData)

    aux = huffmancodec.HuffmanCodec.from_data([1])
    data = list(encodedData) + [aux._eof]
    codec = huffmancodec.HuffmanCodec.from_data(data)
    encoded = codec.encode(data)

    t=codec.get_code_table()

    toWrite = {'t':t, 'd':encoded}
    write_file("encodedPattern.txt", toWrite)

    print("Final size (after huffman): "+str(len(encoded)))

encode()
