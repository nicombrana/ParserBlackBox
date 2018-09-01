def findParamValueAndReplace(aLogLine, anotherLogLine, maxParamValues):
    logLineList = splitTextIntoByToken(aLogLine, " ")
    anotherLogLineList = splitTextIntoByToken(anotherLogLine, " ")
    for index in range(len(logLineList)):
        word = logLineList[index]
        anotherWord = anotherLogLineList[index]
        if word != anotherWord:
            anotherLogLineList[index] = "*"
    structuredLine = " ".join(anotherLogLineList)
    if anotherLogLineList.count("*") > maxParamValues:
        return aLogLine
    return structuredLine


def findParamValueAndReplaceConsideringToken(aLogLine, anotherLogLine, maxParamValues, aToken):
    firstLogLine = splitTextIntoByToken(aLogLine, aToken)
    secondLogLine = splitTextIntoByToken(anotherLogLine, aToken)

    structuredLine = findParamValueAndReplace(firstLogLine[0], secondLogLine[0], maxParamValues)
    structuredLineArray = [structuredLine]
    structuredLineArray.append("")
    structuredLineArray[1] = firstLogLine[1]
    if firstLogLine[1] != secondLogLine[1]:
        structuredLineArray[1] = " *"
    return aToken.join(structuredLineArray)


def haveTheToken(aLogLine, anotherLogLine, aToken):
    return (aLogLine.count(aToken) > 0) & (anotherLogLine.count(aToken) > 0)


def sameLength(aLogLine, anotherLogLine):
    logLineList = splitTextIntoByToken(aLogLine, " ")
    anotherLogLineList = splitTextIntoByToken(anotherLogLine, " ")
    return len(logLineList) == len(anotherLogLineList)


def findParamValueAndReplaceIfSimilarLines(aLogLine, anotherLogLine, maxParamValues):
    if sameLength(aLogLine, anotherLogLine):
        if haveTheToken(aLogLine, anotherLogLine, ":"):
            return findParamValueAndReplaceConsideringToken(aLogLine, anotherLogLine, maxParamValues, ":")
        return findParamValueAndReplace(aLogLine, anotherLogLine, maxParamValues)


def removeTagsFromLineAfterToken(aLogLine, aToken):
    log = splitTextIntoByToken(aLogLine, aToken)
    lastIndex = len(log) - 1
    return "".join(log[lastIndex])


def splitTextIntoByToken(aText, aToken):
    return aText.split(aToken)


def parseLogText(aLogText):
    aLogArray = splitTextIntoByToken(aLogText, "\n")
    aLogLineArray = []
    for logLine in aLogArray:
        aLogLineArray.append(removeTagsFromLineAfterToken(logLine, " : "))
    return compareLogLinesWithin(aLogLineArray)


def compareLogLinesWithin(aLogLineArray):
    structuredLine = ""
    aStructuredLogLineList = []
    for line in aLogLineArray:
        similarLines = list(filter(lambda a: sameLength(line, a), aLogLineArray))
        similarLines.remove(line)
        structuredLine = line
        for similar in similarLines:
            answer = findParamValueAndReplaceIfSimilarLines(line, similar, 2)
            if structuredLine.count("*") < answer.count("*"):
                structuredLine = answer
        aStructuredLogLineList.append(structuredLine)
    return makeSet(aStructuredLogLineList)


def appendWith(aList, anotherList):
    for elem in anotherList:
        aList.append(elem)
    return aList


def makeSet(aList):
    set = []
    for index in range(len(aList)):
        if set.count(aList[index]) == 0:
            set.append(aList[index])
    return set
