import numpy as np
import pickle
import matplotlib.image as mpimg
import Landscape as land



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
    if (type == "wav"):
        if (len(data.shape) == 2):
            return data[:, 0].flatten()
        else:
            return data.flatten()
    if (type == "txt"):
        for letra in data:
            if letra in alfabeto:
                resultado.append(letra)
    return resultado




def shiftsimbolos(fonte, nbits):
    N = len(fonte)
    if (N % 2) != 0:
        N = N - 1
    print("N: ", N)
    fonteInf = np.zeros(int(N / 2))
    k = 0
    count = 0
    for k in range(0, N - 1, 2):
        shiftleft = fonte[k] << nbits
        simbolo = shiftleft + fonte[(k + 1)]
        fonteInf[count] = simbolo
        count = count + 1

    return fonteInf



def Init():
    global buffer
    buffer = str[search_buf_pos:search_buf_pos + search_buf_length]
    for i in buffer:
        encodeArray.append([0, 0, i])
    buffer += str[look_ahead_buf_pos:look_ahead_buf_pos + look_ahead_buf_length]


def MoveForward(step):
    global search_buf_pos, look_ahead_buf_pos, buffer
    search_buf_pos += step;
    look_ahead_buf_pos += step
    buffer = str[search_buf_pos:search_buf_pos + search_buf_length + look_ahead_buf_length]


def Encode():
    sym_offset = search_buf_length
    max_length, max_offset, next_sym = 0, 0, buffer[sym_offset]
    buffer_length = len(buffer)
    if buffer_length - sym_offset == 1:
        encodeArray.append([0, 0, next_sym])
        return max_length
    for offset in range(1, search_buf_length + 1):
        pos = sym_offset - offset
        n = 0
        while buffer[pos + n] == buffer[sym_offset + n]:
            n += 1
            if n == buffer_length - search_buf_length - 1: break
        if max_length < n:
            max_length = n
            max_offset = offset
            next_sym = buffer[sym_offset + n]
    encodeArray.append([max_offset, max_length, next_sym])
    return max_length


def LZ77():
    while 1:
        step = Encode() + 1
        MoveForward(step)
        if look_ahead_buf_pos >= str_length: break


def Decode(encode_lise):
    ans = ''
    for i in encodeArray:
        offset, length, sym = i
        for j in range(length):
            ans += ans[-offset]
        ans += sym
    return ans



def writeListToFile(input):

    with open('teste.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(encodeArray, filehandle)


def convertListofListsToListofStrings(input):
    resultado = []
    fonte=input.copy()
    for array in fonte:
        toAdd=[]
        print(array)
        for elemento in array:
            print(elemento)
            toAdd += [str(elemento)]
        resultado.append(toAdd)
    return resultado




def getEncodedLZ77():
    with open('teste.data', 'rb') as filehandle:
        # read the data as binary data stream
        encodedData = pickle.load(filehandle)
    return encodedData


def convertListofListsToListofStrings(input):
    resultado = []
    fonte=input.copy()
    for array in fonte:
        resultado.append(str(array[0])+","+str(array[1])+","+str(array[2]))
    return resultado

#////////////////////////////////////

alfabeto8bit = list(range(0, 2 ** 8 + 1))

patternData=readFile("data/original/pattern.bmp")
patternData=turnDataIntoArray(patternData,"bmp",alfabeto8bit)

print("Original size: "+str(len(patternData)))

str = land.turnToAscii(patternData)
buffer = ""
search_buf_length, look_ahead_buf_length, str_length = 25, 10, len(str)
search_buf_pos, look_ahead_buf_pos = 0, search_buf_length
encodeArray = []

Init()
LZ77()
print("Size after LZ77: "+str(len(encodeArray)))
writeListToFile(encodeArray)


