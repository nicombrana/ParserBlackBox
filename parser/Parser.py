import re


lineSeparatorToken = "\n"
wildcardToken = "*"
valueSeparatorToken = ": "
tokenList = [': ', '=', " - "]
timestampExpression = '\d{4}-\d{2}-\d{2}-\d{2}:\d{2}:\d{2}.\d{3}'
#'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}' For small logs


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
    tokenCount = 0
    for similar in aListOfLines:
        answer = structurizedSimilarLines(aLine, similar, 2)
        if tokenCount < answer.count(wildcardToken):
            structuredLine = answer
            tokenCount = structuredLine.count(wildcardToken)
    return structuredLine


def hasMoreTokens(aStructuredLine, anotherAnswer):
    firstLine = aStructuredLine
    secondLine = anotherAnswer
    if bothHaveTheToken(aStructuredLine, anotherAnswer, valueSeparatorToken):
        a = splitTextIntoByToken(aStructuredLine, valueSeparatorToken)
        firstLine = a[0]
        b = splitTextIntoByToken(anotherAnswer, valueSeparatorToken)
        secondLine = b[0]
    return firstLine.count(wildcardToken) < secondLine.count(wildcardToken)


def structurizedSimilarLines(aLogLine, anotherLogLine, maxParamValues):
    cantTokens = maxParamValues + tokenCount(aLogLine)
    if hasToken(aLogLine, valueSeparatorToken) and hasToken(anotherLogLine, valueSeparatorToken):
        return structurizedLogLineConsideringToken(aLogLine, anotherLogLine, maxParamValues, valueSeparatorToken)
    if hasToken(aLogLine, '{') and hasToken(anotherLogLine, '{'):
        return structurizedObjectLogLines(aLogLine, anotherLogLine, maxParamValues, ['{', '}'])
    if hasToken(aLogLine, '[') and hasToken(anotherLogLine, '['):
        return structurizedObjectLogLines(aLogLine, anotherLogLine, maxParamValues, ['[', ']'])
    if not(hasToken(aLogLine, valueSeparatorToken)) & (not(hasToken(anotherLogLine, valueSeparatorToken))):
        return structurizedLogLines(aLogLine, anotherLogLine, cantTokens)


def structurizedObjectLogLines(aLogLine, anotherLogLine, maxParamValues, tokens):
    aLineArray = splitTextIntoByToken(aLogLine, tokens[0])
    anotherLineArray = splitTextIntoByToken(anotherLogLine, tokens[0])
    aL = removeTagsFromLineAfterToken(aLogLine, tokens[1])
    anotherL = removeTagsFromLineAfterToken(anotherLogLine, tokens[1])

    aLineArray[1] = aL
    anotherLineArray[1] = anotherL

    structuredLine = []
    structuredLine.append(structurizedSimilarLines(aLineArray[0], anotherLineArray[0], maxParamValues))
    structuredLine.append(wildcardToken)
    structuredLine[1] += (tokens[1])
    structuredLine[1] += structurizedSimilarLines(aLineArray[1], anotherLineArray[1], maxParamValues)
    return tokens[0].join(structuredLine)


def structurizedLogLineConsideringToken(aLogLine, anotherLogLine, maxParamValues, aToken):
    firstLogLine = splitTextIntoByToken(aLogLine, aToken)
    secondLogLine = splitTextIntoByToken(anotherLogLine, aToken)
    cantTokens = 1 + tokenCount(firstLogLine[0])
    structuredLine = structurizedLogLines(firstLogLine[0], secondLogLine[0], cantTokens)

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
    if hasToken(aLogLine, valueSeparatorToken) and hasToken(anotherLogLine, valueSeparatorToken):
        aLine = splitTextIntoByToken(aLogLine, valueSeparatorToken)
        aLine = splitTextIntoByToken(aLine[0], " ")
        anotherLine = splitTextIntoByToken(anotherLogLine, valueSeparatorToken)
        anotherLine = splitTextIntoByToken(anotherLine[0], " ")
        return len(aLine) == len(anotherLine)
    if hasToken(aLogLine, '{') and hasToken(anotherLogLine, '{'):
        return sameLengthConsideringTokens(aLogLine, anotherLogLine, ['{', '}'])
    if hasToken(aLogLine, '[') and hasToken(anotherLogLine, ']'):
        return sameLengthConsideringTokens(aLogLine, anotherLogLine, ['[', ']'])
    if not(hasToken(aLogLine, valueSeparatorToken)) & (not(hasToken(anotherLogLine, valueSeparatorToken))):
        logLineList = splitTextIntoByToken(aLogLine, " ")
        anotherLogLineList = splitTextIntoByToken(anotherLogLine, " ")
        return len(logLineList) == len(anotherLogLineList)
    return False


def sameLengthConsideringTokens(aLogLine, anotherLogLine, tokens):
    aLineFirstPart = splitTextIntoByToken(aLogLine, tokens[0])
    anotherLineFirstPart = splitTextIntoByToken(anotherLogLine, tokens[0])
    aLFirst = splitTextIntoByToken(aLineFirstPart[0], " ")
    anLFirst = splitTextIntoByToken(anotherLineFirstPart[0], " ")

    aLineSecondPart = removeTagsFromLineAfterToken(aLogLine, tokens[1])
    anotherLineSecondPart = removeTagsFromLineAfterToken(anotherLogLine, tokens[1])

    return (len(aLFirst) == len(anLFirst)) and sameLength(aLineSecondPart, anotherLineSecondPart)


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
    timestamp = re.search(timestampExpression, aLine)
    if timestamp is not None:
        return timestamp.group()
    return ""


def tokenCount(aLine):
    tokenCount = 0
    for token in tokenList:
        tokenCount += aLine.count(token)
    return tokenCount
