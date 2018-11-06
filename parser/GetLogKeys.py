#!/bin/python3
import Parser
import datetime
import sys
import os
import concurrent.futures
import multiprocessing


LogFileName = sys.argv[1]
FreeTextFileName = LogFileName + "FreeText"
StructuredLogFileName = sys.argv[2]
freeTextSeparatorToken = sys.argv[3]
maxWorkers = multiprocessing.cpu_count()

#NotInUse
#def parseFullLogText(aLogText):
#    aFreeTextLog = keepFreeText(aLogText, freeTextSeparatorToken)
#    aLogLineArray = lineSeparatorToken.join(aFreeTextLog)
#    return parseFreeText(aLogLineArray, valueSeparatorToken)


def parseLogFile():
    generateFreeTextLog(LogFileName)
    parseFreeTextByChunks()


def generateFreeTextLog(aCompleteLogFileName):
    print("Remove Metadata and Generate FreeText Log")
    print(datetime.datetime.now().time())
    logFile = open(aCompleteLogFileName, encoding="ISO-8859-1")
    freeTextLog = open(FreeTextFileName, 'w')
    Parser.readLines(logFile, 3)
    for line in logFile:
        freeText = Parser.removeTagsFromLineAfterToken(line, freeTextSeparatorToken)
        freeTextLog.write(freeText)
    freeTextLog.close()
    logFile.close()
    print(datetime.datetime.now().time())
    print("Metada Removed and FreeText Log Generated")


def parseFreeTextByChunks():
    print("Begin Parsing")
    print(datetime.datetime.now().time())
    logKey = []
    freeTextFile = open(FreeTextFileName, 'r')

    print("Initialize Parsing 1 Chunk")
    print(datetime.datetime.now().time())
    firstChunk = Parser.readLines(freeTextFile, 512)
    logKey = Parser.parseFreeText(firstChunk)
    print(datetime.datetime.now().time())
    print("Parsing 1 Chunk Completed")

    print("Begin Reduction of File by Chunks against the 1 Parsed Chunk")
    print(datetime.datetime.now().time())
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        for f in executor.map(lambda a: Parser.compareLogs(logKey, a), Parser.readInChunks(freeTextFile)):
            newLines = list(f)
            Parser.appendWith(logKey, newLines)
    freeTextFile.close()
    print(datetime.datetime.now().time())
    print("Reduction of File by Chunks against the 1 Parsed Chunk Completed")

    print("Begin Elimination of Particular Cases")
    print(datetime.datetime.now().time())
    finalLogKeys = Parser.parseArray(logKey)
    print(datetime.datetime.now().time())
    print("Elimination Completed")

    structuredLogFile = open(StructuredLogFileName, 'w')
    structuredLogFile.write(Parser.lineSeparatorToken.join(finalLogKeys))
    structuredLogFile.close()
    os.remove(FreeTextFileName)
    print(datetime.datetime.now().time())
    print("Parsing Completed")


parseLogFile()
