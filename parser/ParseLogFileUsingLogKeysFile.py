#!/bin/python3
import Parser
import datetime
import sys
import concurrent.futures


aLogFileName = sys.argv[1]
aLogKeysFileName = sys.argv[2]
aFileNameForSaving = sys.argv[3]


def parseLogUsingLogKeys():
    logKeys = Parser.splitTextIntoByToken(openAndReadFile(aLogKeysFileName), Parser.lineSeparatorToken)
    print("Parsing New Log Initialize")
    print(datetime.datetime.now().time())
    aNewLog = open(aFileNameForSaving, "w+")
    aLogFile = open(aLogFileName, 'r')
    aTimeStampFile = open(aFileNameForSaving + 'Timestamp', "w+")
    Parser.readLines(aLogFile, 3)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for f in executor.map(lambda a: workTheChunksWithLogKeys(a, logKeys), Parser.readInChunks(aLogFile)):
            newLines = list(f)
            aTimeStampFile.write(newLines[0])
            aNewLog.write(newLines[1])
    aTimeStampFile.close()
    aLogFile.close()
    aNewLog.close()
    print(datetime.datetime.now().time())
    print("Parsing New Log Completed")


def workTheChunksWithLogKeys(aLogChunk, logKeys):
    timeStamps = Parser.keepTimestamp(aLogChunk)
    freeText = Parser.keepFreeText(aLogChunk, Parser.freeTextSeparatorToken)
    parsedLines = []
    for aLogLine in freeText:
        parsedLines.append(findLogKeyFor(aLogLine, logKeys))
    log = []
    log.append(timeStamps)
    log.append("\n".join(parsedLines))
    return log


def parseFileAgainstLogKeys(aLogLine, aLogKeysLog):
    aLogLineArray = Parser.keepFreeText(aLogLine, Parser.freeTextSeparatorToken)
    logKey = findLogKeyFor(aLogLineArray[0], aLogKeysLog)
    return logKey


def findLogKeyFor(aLogLine, aLogKeyLog):
    return getLogKeyFor(aLogLine, aLogKeyLog)


def getLogKeyFor(aLogLine, aLogKeysLog):
    logKeys = Parser.getSimilarLines(aLogLine, aLogKeysLog)
    return Parser.getStructuredLine(aLogLine, logKeys)


def openAndReadFile(aFileName):
    aFile = open(aFileName, 'r')
    aFileContent = aFile.read()
    aFile.close()
    return aFileContent
