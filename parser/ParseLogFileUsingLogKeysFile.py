#!/bin/python3
import Parser
import datetime
import sys


aLogFileName = sys.argv[1]
aLogKeysFileName = sys.argv[2]
aFileNameForSaving = sys.argv[3]


def parseLogUsingLogKeys():
    logKeys = Parser.splitTextIntoByToken(openAndReadFile(aLogKeysFileName), Parser.lineSeparatorToken)
    print("Parsing New Log Initialize")
    print(datetime.datetime.now().time())
    aNewLog = open(aFileNameForSaving, "w+")
    aLogFile = open(aLogFileName, 'r')
    for aLogChunk in Parser.readInChunks(aLogFile):
        freeText = Parser.keepFreeText(aLogChunk, Parser.freeTextSeparatorToken)
        for aLogLine in freeText:
            parsedLogLine = findLogKeyFor(aLogLine, logKeys)
            aNewLog.write(parsedLogLine)
            aNewLog.write(Parser.lineSeparatorToken)
    aLogFile.close()
    aNewLog.close()
    print(datetime.datetime.now().time())
    print("Parsing New Log Completed")


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
