from random import randint
import math
import numpy as np
from tqdm import tqdm

ALPHABET_LENGTH = 4
SAMPLES_NUMBER = 400

SHOW_GENERATED_MESSAGE = True
SHOW_DICTIONARY = True
SHOW_ENCODED_MESSAGE = True

def sourceGenerator(alphabetLength, codeLength):
    generatedCode = [str(randint(0, alphabetLength-1)) for i in range(codeLength)]
    return ''.join(generatedCode)

def buildLZDictionary(inputCode):
    LZDictionary = {}

    sequenceStart = 0

    for i in tqdm(range(len(inputCode))):
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
    for element in tqdm(dictionary):
        pointerToElement = 0
        if(len(element) > 1):
            if(element[:-1] in dictionary):
                pointerToElement = list(dictionary).index(element[:-1]) + 1
        encodedMessage += str(bin(pointerToElement))[2:].rjust(maximumAddressLength, "0")
        encodedMessage += str(bin(int(element[-1])))[2:].rjust(maximumValueLength, "0")

    return encodedMessage

def LZLemmaValidator(dictionary, samplesNumber):
    log2n = math.log2(samplesNumber)
    epsilon = (math.log2(log2n + 2)+2)/log2n

    return len(dictionary) <= samplesNumber/((1-epsilon)*log2n)

print("Generating source message...")
codeToCompress = sourceGenerator(ALPHABET_LENGTH, SAMPLES_NUMBER)

if(SHOW_GENERATED_MESSAGE):
    print(f"SOURCE GENERATED CODE: {codeToCompress}")

print("Building Lempel-Ziv dictionary...")
LZDictionary = buildLZDictionary(codeToCompress)

if(SHOW_DICTIONARY):
    print(f"LEMPEL-ZIV DICTIONARY: {LZDictionary}")

print("Encoding...")
encodedMessage = LZEncode(LZDictionary, ALPHABET_LENGTH)

print(f"ENCODED MESSAGE LENGTH: {len(encodedMessage)} bits.")

if(SHOW_ENCODED_MESSAGE):
    print(f"ENCODED MESSAGE (length={len(encodedMessage)} bits): {encodedMessage}")

print(f"Lempel-Ziv Lemma Validation: {LZLemmaValidator(LZDictionary, SAMPLES_NUMBER)}")

print("Encoding completed.")