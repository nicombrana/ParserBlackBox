#!/bin/python3
import Parser
import datetime
import sys
import concurrent.futures


aLogFileName = sys.argv[1]
aLogKeysFileName = sys.argv[2]
freeTextSeparatorToken = sys.argv[3]
aFileNameForSaving = aLogFileName + "LogLyzed"
logKeys = []


def parseLogUsingLogKeys():
    global logKeys
    logKeys = Parser.splitTextIntoByToken(openAndReadFile(aLogKeysFileName), Parser.lineSeparatorToken)
    print("Parsing New Log Initialize")
    print(datetime.datetime.now().time())
    aNewLog = open(aFileNameForSaving, "w+")
    aLogFile = open(aLogFileName, 'r')
    aTimeStampFile = open(aFileNameForSaving + 'Timestamp', "w+")
    Parser.readLines(aLogFile, 3)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for f in executor.map(lambda a: parseChunksWithLogKeys(a, logKeys), Parser.readInChunks(aLogFile)):
            newLines = list(f)
            aTimeStampFile.write(newLines[0])
            aNewLog.write(newLines[1])
    aTimeStampFile.close()
    aLogFile.close()
    aNewLog.close()
    logKeysFile = open(aLogKeysFileName, 'w')
    logKeys = Parser.appendAndCompareLogs(logKeys, [])
    logKeysFile.write("\n".join(logKeys))
    logKeysFile.close()
    print(datetime.datetime.now().time())
    print("Parsing New Log Completed")


def parseChunksWithLogKeys(aLogChunk, aLogKeys):
    timeStamps = Parser.keepTimestamp(aLogChunk)
    freeText = Parser.keepFreeText(aLogChunk, freeTextSeparatorToken)
    parsedLines = []
    for aLogLine in freeText:
        parsedLines.append(findLogKeyFor(aLogLine, aLogKeys))
    log = []
    log.append(timeStamps)
    log.append("\n".join(parsedLines))
    return log


def parseFileAgainstLogKeys(aLogLine, aLogKeysLog):
    aLogLineArray = Parser.keepFreeText(aLogLine, freeTextSeparatorToken)
    logKey = findLogKeyFor(aLogLineArray[0], aLogKeysLog)
    return logKey


def findLogKeyFor(aLogLine, aLogKeyLog):
    return getLogKeyFor(aLogLine, aLogKeyLog)


def getLogKeyFor(aLogLine, aLogKeysLog):
    someKeys = Parser.getSimilarLines(aLogLine, aLogKeysLog)
    answer = Parser.getStructuredLine(aLogLine, someKeys)
    if aLogLine == answer or aLogKeysLog.count(answer) == 0:
        global logKeys
        logKeys.append(answer)
    return answer
#Trying to make it learn new logs(?)


def openAndReadFile(aFileName):
    aFile = open(aFileName, 'r')
    aFileContent = aFile.read()
    aFile.close()
    return aFileContent
