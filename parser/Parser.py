import datetime
import sys
import os
import concurrent.futures
import multiprocessing
import re


LogFileName = sys.argv[1]
FreeTextFileName = LogFileName + "FreeText"
StructuredLogFileName = sys.argv[2]
freeTextSeparatorToken = sys.argv[3]
lineSeparatorToken = "\n"
wildcardToken = "*"
valueSeparatorToken = ": "
tokenList = [": ", "="]
maxWorkers = multiprocessing.cpu_count()


def parseFullLogText(aLogText):
    aFreeTextLog = keepFreeText(aLogText, freeTextSeparatorToken)
    aLogLineArray = lineSeparatorToken.join(aFreeTextLog)
    return parseFreeText(aLogLineArray, valueSeparatorToken)


def parseLogFile():
    generateFreeTextLog(LogFileName)
    parseFreeTextByChunks()


def parseFreeTextByChunks():
    print("Begin Parsing")
    print(datetime.datetime.now().time())
    logKey = []
    freeTextFile = open(FreeTextFileName, 'r')

    print("Initialize Parsing 1 Chunk")
    print(datetime.datetime.now().time())
    firstChunk = readLines(freeTextFile, 512)
    logKey = parseFreeText(firstChunk)
    print(datetime.datetime.now().time())
    print("Parsing 1 Chunk Completed")

    print("Begin Reduction of File by Chunks against the 1 Parsed Chunk")
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        for f in executor.map(lambda a: compareLogs(logKey, a), readInChunks(freeTextFile)):
            newLines = list(f)
            appendWith(logKey, newLines)
    freeTextFile.close()
    print(datetime.datetime.now().time())
    print("Reduction of File by Chunks against the 1 Parsed Chunk Completed")

    print("Begin Elimination of Particular Cases")
    print(datetime.datetime.now().time())
    finalLogKeys = parseArray(logKey)
    print(datetime.datetime.now().time())
    print("Elimination Completed")

    structuredLogFile = open(StructuredLogFileName, 'w')
    structuredLogFile.write(lineSeparatorToken.join(finalLogKeys))
    structuredLogFile.close()
    os.remove(FreeTextFileName)
    print(datetime.datetime.now().time())
    print("Parsing Completed")


def readInChunks(aFile, lines_ammount=256):
    while True:
        chunk = readLines(aFile, lines_ammount)
        if not chunk:
            break
        yield chunk


def readLines(aFile, anAmmountOfLines):
    lines = ""
    times = 1
    while times <= anAmmountOfLines:
        lines += aFile.readline()
        times += 1
    return lines


def generateFreeTextLog(aCompleteLogFileName):
    print("Remove Metadata and Generate FreeText Log")
    print(datetime.datetime.now().time())
    logFile = open(aCompleteLogFileName, encoding="ISO-8859-1")
    freeTextLog = open(FreeTextFileName, 'w')
    readLines(logFile, 3)
    for line in logFile:
        freeText = removeTagsFromLineAfterToken(line, freeTextSeparatorToken)
        freeTextLog.write(freeText)
    freeTextLog.close()
    logFile.close()
    print(datetime.datetime.now().time())
    print("Metada Removed and FreeText Log Generated")


def parseFreeText(aLogChunk):
    aLogLineArray = splitTextIntoByToken(aLogChunk, lineSeparatorToken)
    return parseArray(aLogLineArray)


def parseArray(aLogLineArray):
    structuredLine = ""
    aStructuredLogLineList = []
    for line in aLogLineArray:
        wasLineAlready = any(matchesStructuredLine(line, logKey) for logKey in aStructuredLogLineList)
        if not(wasLineAlready):
            similarLines = getSimilarLines(line, aLogLineArray)
            similarLines.remove(line)
            structuredLine = getStructuredLine(line, similarLines)
            aStructuredLogLineList.append(structuredLine)
    return makeSet(aStructuredLogLineList)


def compareLogs(aLogKeyArray, aLogLines):
    aLogArray = splitTextIntoByToken(aLogLines, lineSeparatorToken)
    output = []
    for line in aLogArray:
        exists = any(matchesStructuredLine(line, logKey) for logKey in aLogKeyArray)
        if not(exists):
            similarLines = getSimilarLines(line, aLogArray)
            structuredLine = getStructuredLine(line, similarLines)
            output.append(structuredLine)
    return output


def appendAndCompareLogs(aLogLine, anotherLogLine):
    newLogLineArray = appendWith(aLogLine, anotherLogLine)
    newLogLine = lineSeparatorToken.join(newLogLineArray)
    return parseFreeText(newLogLine)


def matchesStructuredLine(aLine, aStructuredLine):
    if sameLength(aLine, aStructuredLine):
        return getStructuredLine(aLine, [aStructuredLine]) == aStructuredLine
    return False


def getSimilarLines(aLine, aLineArray):
    return list(filter(lambda a: sameLength(aLine, a), aLineArray))


def getStructuredLine(aLine, aListOfLines):
    structuredLine = aLine
    for similar in aListOfLines:
        answer = structurizedSimilarLines(aLine, similar, 2)
        if structuredLine.count(wildcardToken) < answer.count(wildcardToken):
            structuredLine = answer
    return structuredLine


def structurizedSimilarLines(aLogLine, anotherLogLine, maxParamValues):
    if bothHaveTheToken(aLogLine, anotherLogLine, valueSeparatorToken):
        return structurizedLogLineConsideringToken(aLogLine, anotherLogLine, maxParamValues, valueSeparatorToken)
    if not(hasToken(aLogLine, valueSeparatorToken)) & (not(hasToken(anotherLogLine, valueSeparatorToken))):
        return structurizedLogLines(aLogLine, anotherLogLine, maxParamValues)


def structurizedLogLineConsideringToken(aLogLine, anotherLogLine, maxParamValues, aToken):
    firstLogLine = splitTextIntoByToken(aLogLine, aToken)
    secondLogLine = splitTextIntoByToken(anotherLogLine, aToken)

    structuredLine = structurizedLogLines(firstLogLine[0], secondLogLine[0], 1)

    structuredLineArray = [structuredLine]
    structuredLineArray.append(wildcardToken)
    return aToken.join(structuredLineArray)


def structurizedLogLines(aLogLine, anotherLogLine, maxParamValues):
    logLineList = splitTextIntoByToken(aLogLine, " ")
    anotherLogLineList = splitTextIntoByToken(anotherLogLine, " ")
    structuredLine = structurizedLineList(logLineList, anotherLogLineList)
    if structuredLine.count(wildcardToken) > maxParamValues:
        return aLogLine
    return structuredLine


def structurizedLineList(aLineList, anotherLineList):
    structuredLineList = []
    for index in range(len(aLineList)):
        aWord = aLineList[index]
        anotherWord = anotherLineList[index]
        structuredLineList.append(structurizedIfEqualWords(aWord, anotherWord))
    return " ".join(structuredLineList)


def structurizedIfEqualWords(aWord, anotherWord):
    if aWord != anotherWord:
        return wildcardToken
    return aWord


def bothHaveTheToken(aLogLine, anotherLogLine, aToken):
    answer = False
    for token in tokenList:
        answer = answer or (hasToken(aLogLine, token) & hasToken(anotherLogLine, token))
    return answer


def hasToken(aLogLine, aToken):
    return (aLogLine.count(aToken) > 0)


def sameLength(aLogLine, anotherLogLine):
    if (bothHaveTheToken(aLogLine, anotherLogLine, valueSeparatorToken)):
        aLine = splitTextIntoByToken(aLogLine, valueSeparatorToken)
        aLine = splitTextIntoByToken(aLine[0], " ")
        anotherLine = splitTextIntoByToken(anotherLogLine, valueSeparatorToken)
        anotherLine = splitTextIntoByToken(anotherLine[0], " ")
        return len(aLine) == len(anotherLine)
    if not(hasToken(aLogLine, valueSeparatorToken)) & (not(hasToken(anotherLogLine, valueSeparatorToken))):
        logLineList = splitTextIntoByToken(aLogLine, " ")
        anotherLogLineList = splitTextIntoByToken(anotherLogLine, " ")
        return len(logLineList) == len(anotherLogLineList)
    return False


def keepFreeText(aLogText, aToken):
    aLogArray = splitTextIntoByToken(aLogText, lineSeparatorToken)
    aLogLineArray = []
    for logLine in aLogArray:
        aLogLineArray.append(removeTagsFromLineAfterToken(logLine, aToken))
    return aLogLineArray


def removeTagsFromLineAfterToken(aLogLine, aToken):
    aLogArray = splitTextIntoByToken(aLogLine, aToken)
    aLogArray.remove(aLogArray[0])
    return aToken.join(aLogArray)


def splitTextIntoByToken(aText, aToken):
    return aText.split(aToken)


def makeSet(aList):
    set = []
    for index in range(len(aList)):
        if set.count(aList[index]) == 0:
            set.append(aList[index])
    return set


def appendWith(aList, anotherList):
    for elem in anotherList:
        aList.append(elem)
    return aList


def keepTimestamp(aLogText):
    aLogArray = splitTextIntoByToken(aLogText, lineSeparatorToken)
    aTimeStampArray = []
    for logLine in aLogArray:
        aTimeStampArray.append(getTimeStampFrom(logLine))
    return "\n".join(aTimeStampArray)


def getTimeStampFrom(aLine):
    r = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}')
    lineArray = splitTextIntoByToken(aLine, " ")
    timeStamp = []
    if len(lineArray) > 2:
        timeStamp.append(lineArray[1])
        timeStamp.append(lineArray[2])
    timeStamp = " ".join(timeStamp)
    if r.match(timeStamp):
        return timeStamp
    return ""


def tokenCount(aLine):
    tokenCount = 0
    for token in tokenList:
        tokenCount += aLine.count(token)
    return tokenCount
