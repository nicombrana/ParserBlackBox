import datetime
import functools
import concurrent.futures
import multiprocessing


freeTextFileName = "FreeTextLog.txt"
structuredLogFileName = "StructuredLog.txt"
lineSeparatorToken = "\n"
freeTextSeparatorToken = " - "
wildcardToken = "*"
valueSeparatorToken = ":"
valueWildcardToken = " *"
maxWorkers = multiprocessing.cpu_count()


def parseFullLogText(aLogText):
    aFreeTextLog = keepFreeText(aLogText, freeTextSeparatorToken)
    aLogLineArray = lineSeparatorToken.join(aFreeTextLog)
    return parseFreeText(aLogLineArray, valueSeparatorToken)


def parseLogFile(aCompleteLogFileName):
    generateFreeTextLog(aCompleteLogFileName)
    parseFreeTextByChunks()


def parseFreeTextByChunks():
    print("Begin Parsing")
    print(datetime.datetime.now().time())
    logKey = []
    freeTextFile = open(freeTextFileName, 'r')

    print("Initialize Parsing 1 Chunk")
    print(datetime.datetime.now().time())
    freeText.readline()
    freeText.readLine()
    freeText.readLine()
    firstChunk = freeTextFile.read(8388608)
    logKey = parseFreeText(firstChunk, valueSeparatorToken)
    print(datetime.datetime.now().time())
    print("Parsing 1 Chunk Completed")

    #reduce the next chunks against the already parsed one.
    print("Begin Reduction of Fille by Chunks against the 1 Parsed Chunk")
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
        for f in executor.map(lambda a: compareLogs(logKey, a, valueSeparatorToken), readInChunks(freeTextFile)):
            newLines = list(f)
            appendWith(logKey, newLines)
    print(datetime.datetime.now().time())
    print("Reduction of File by Chunks against the 1 Parsed Chunk Completed")

    print("Begin Elimination of Particular Cases")
    print(datetime.datetime.now().time())
    logKey = parseArray(logKey, valueSeparatorToken)
    print(datetime.datetime.now().time())
    print("Elimination Completed")

    structuredLogFile = open(structuredLogFileName, 'w')
    structuredLogFile.write(lineSeparatorToken.join(logKey))
    structuredLogFile.close()
    print(datetime.datetime.now().time())
    print("Parsing Completed")


def readInChunks(aFile, chunk_size=8388608):
    while True:
        chunk = aFile.read(chunk_size)
        if not chunk:
            break
        yield chunk


def generateFreeTextLog(aCompleteLogFileName):
    print("Remove Metadata and Generate FreeText Log")
    logFile = open(aCompleteLogFileName, encoding="ISO-8859-1")
    freeTextLog = open(freeTextFileName, 'w')
    for line in logFile:
        freeText = removeTagsFromLineAfterToken(line, freeTextSeparatorToken)
        freeTextLog.write(freeText)
    freeTextLog.close()
    logFile.close()
    print("Metada Removed and FreeText Log Generated")


def parseFreeText(aLogChunk, aToken):
    aLogLineArray = splitTextIntoByToken(aLogChunk, lineSeparatorToken)
    return parseArray(aLogLineArray, aToken)


def parseArray(aLogLineArray, aToken)
    structuredLine = ""
    aStructuredLogLineList = []
    withoutTokens = list(filter(lambda aLine: not(hasToken(aLine, aToken)), aLogLineArray))
    withToken = list(filter(lambda aLine: aLine.count(aToken) == 1, aLogLineArray))
    withMoreThanOneToken = list(filter(lambda aLine: aLine.count(aToken) > 1, aLogLineArray))
    group = [withoutTokens, withToken, withMoreThanOneToken]
    for array in group:
        for line in aLogLineArray:
            wasLineAlready = any(matchesStructuredLine(line, logKey, aToken) for logKey in aStructuredLogLineList)
            if not(wasLineAlready):
                similarLines = getSimilarLines(line, aLogLineArray, aToken)
                similarLines.remove(line)
                structuredLine = getStructuredLine(line, similarLines, aToken)
                aStructuredLogLineList.append(structuredLine)
    return makeSet(aStructuredLogLineList)

# Create abstraction
def compareLogs(aLogKeyArray, aLogLines, aToken):
    aLogArray = splitTextIntoByToken(aLogLines, lineSeparatorToken)
    output = []
    for line in aLogArray:
        exists = any(matchesStructuredLine(line, logKey, aToken) for logKey in aLogKeyArray)
        if not(exists):
            similarLines = getSimilarLines(line, aLogKeyArray, aToken)
            structuredLine = getStructuredLine(line, similarLines, aToken)
            output.append(structuredLine)
    return output


def appendAndCompareLogs(aLogLine, anotherLogLine, aToken):
    newLogLineArray = appendWith(aLogLine, anotherLogLine)
    newLogLine = lineSeparatorToken.join(newLogLineArray)
    return parseFreeText(newLogLine, aToken)


def matchesStructuredLine(aLine, aStructuredLine, aToken):
    if sameLength(aLine, aStructuredLine, aToken):
        return getStructuredLine(aLine, [aStructuredLine], aToken) == aStructuredLine
    return False


def getSimilarLines(aLine, aLineArray, aToken):
    return list(filter(lambda a: sameLength(aLine, a, aToken), aLineArray))


def getStructuredLine(aLine, aListOfLines, aToken):
    structuredLine = aLine
    for similar in aListOfLines:
        answer = structurizedSimilarLines(aLine, similar, 2, aToken)
        if structuredLine.count(wildcardToken) < answer.count(wildcardToken):
            structuredLine = answer
    return structuredLine


def structurizedSimilarLines(aLogLine, anotherLogLine, maxParamValues, aToken):
    if bothHaveTheToken(aLogLine, anotherLogLine, aToken):
        return structurizedLogLineConsideringToken(aLogLine, anotherLogLine, maxParamValues, aToken)
    if not(hasToken(aLogLine, aToken)) & (not(hasToken(anotherLogLine, aToken))):
        return structurizedLogLines(aLogLine, anotherLogLine, maxParamValues)


def structurizedLogLineConsideringToken(aLogLine, anotherLogLine, maxParamValues, aToken):
    firstLogLine = splitTextIntoByToken(aLogLine, aToken)
    secondLogLine = splitTextIntoByToken(anotherLogLine, aToken)

    structuredLine = structurizedLogLines(firstLogLine[0], secondLogLine[0], maxParamValues)

    structuredLineArray = [structuredLine]
    structuredLineArray.append("")
    structuredLineArray[1] = firstLogLine[1]
    if firstLogLine[1] != secondLogLine[1]:
        structuredLineArray[1] = valueWildcardToken
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
    return hasToken(aLogLine, aToken) & hasToken(anotherLogLine, aToken)


def hasToken(aLogLine, aToken):
    return (aLogLine.count(aToken) > 0)


def sameLength(aLogLine, anotherLogLine, aToken):
    if (bothHaveTheToken(aLogLine, anotherLogLine, aToken)):
        aLine = splitTextIntoByToken(aLogLine, aToken)
        aLine = splitTextIntoByToken(aLine[0], " ")
        anotherLine = splitTextIntoByToken(anotherLogLine, aToken)
        anotherLine = splitTextIntoByToken(anotherLine[0], " ")
        return len(aLine) == len(anotherLine)
    if not(hasToken(aLogLine, aToken)) & (not(hasToken(anotherLogLine, aToken))):
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
    log = splitTextIntoByToken(aLogLine, aToken)
    lastIndex = len(log) - 1
    return "".join(log[lastIndex])


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


parseLogFile("sep15")
