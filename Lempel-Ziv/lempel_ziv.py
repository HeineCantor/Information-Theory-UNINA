from random import randint
import math
import numpy as np

ALPHABET_LENGTH = 4
SAMPLES_NUMBER = 50

def sourceGenerator(alphabetLength, codeLength):
    generatedCode = [str(randint(0, alphabetLength-1)) for i in range(codeLength)]
    return ''.join(generatedCode)

def buildLZDictionary(inputCode):
    LZDictionary = {}

    sequenceStart = 0

    for i in range(len(inputCode)):
        potentialPhrase = inputCode[sequenceStart : i + 1]
        if (potentialPhrase not in LZDictionary):
            LZDictionary[potentialPhrase] = len(LZDictionary) + 1
            sequenceStart = i + 1

    if sequenceStart < len(inputCode): # you lost some final characters
        lastElement = LZDictionary.popitem()
        newKey = lastElement[0] + inputCode[sequenceStart : len(inputCode)]
        LZDictionary[newKey] = lastElement[1]


    return LZDictionary
    
def LZEncode(dictionary, alphabetLength):
    encodedMessage = ""
    maximumAddressLength = math.floor(math.log2(len(dictionary))) + 1
    maximumValueLength = math.floor(math.log2(alphabetLength))
    for element in dictionary:
        pointerToElement = 0
        if(len(element) > 1):
            pointerToElement = list(dictionary).index(element) + 1
        encodedMessage += str(bin(pointerToElement))[2:].rjust(maximumAddressLength, "0")
        encodedMessage += str(bin(int(element[-1])))[2:].rjust(maximumValueLength, "0")

    return encodedMessage


codeToCompress = sourceGenerator(ALPHABET_LENGTH, SAMPLES_NUMBER)

print(f"SOURCE GENERATED CODE: {codeToCompress}")

LZDictionary = buildLZDictionary(codeToCompress)

print(f"LEMPEL-ZIV DICTIONARY: {LZDictionary}")

encodedMessage = LZEncode(LZDictionary, ALPHABET_LENGTH)

print(f"ENCODED MESSAGE (length={len(encodedMessage)} bits): {encodedMessage}")