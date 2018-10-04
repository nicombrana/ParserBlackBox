#!/bin/python3
import PossibleParser as Parser
import datetime
import sys


def parseLogUsingLogKeys():
    aLogFileName = sys.argv[1]
    aLogKeysFileName = sys.argv[2]
    logKeys = Parser.splitTextIntoByToken(openAndReadFile(aLogKeysFileName), Parser.lineSeparatorToken)
    print("Parsing New Log Initialize")
    print(datetime.datetime.now().time())
    aFileNameForSaving = sys.argv[3]
    aNewLog = open(aFileNameForSaving, "w+")
    with open(aLogFileName, 'r') as aLog:
        for aLogLine in aLog:
            parsedLogLine = parseFileAgaisntLogKeys(aLogLine, logKeys)
            aNewLog.write(parsedLogLine)
            aNewLog.write(Parser.lineSeparatorToken)
    aLog.close()
    aNewLog.close()
    print(datetime.datetime.now().time())
    print("Parsing New Log Completed")


def parseFileAgaisntLogKeys(aLogLine, aLogKeysLog):
    aLogLineArray = Parser.keepFreeText(aLogLine, Parser.freeTextSeparatorToken)
    logKey = findLogKeyFor(aLogLineArray[0], aLogKeysLog, Parser.valueSeparatorToken)
    return logKey


def findLogKeyFor(aLogLine, aLogKeyLog, aToken):
    return getLogKeyFor(aLogLine, aLogKeyLog, aToken)


def getLogKeyFor(aLogLine, aLogKeysLog, aToken):
    logKeys = Parser.getSimilarLines(aLogLine, aLogKeysLog, aToken)
    return Parser.getStructuredLine(aLogLine, logKeys, aToken)


def openAndReadFile(aFileName):
    print(aFileName)
    aFile = open(aFileName, 'r')
    aFileContent = aFile.read()
    aFile.close()
    return aFileContent


parseLogUsingLogKeys()
