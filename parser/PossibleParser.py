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
        return ""
    return structuredLine


def findParamValueAndReplaceConsideringToken(aLogLine, anotherLogLine, maxParamValues, aToken):
    firstLogLine = splitTextIntoByToken(aLogLine, aToken)
    secondLogLine = splitTextIntoByToken(anotherLogLine, aToken)

    structuredLine = findParamValueAndReplace(firstLogLine[0], secondLogLine[0], maxParamValues)
    structuredLineArray = [structuredLine]
    structuredLineArray.append("")
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
    finalVector = []
    for logLine in aLogArray:
        aLogLineArray.append(removeTagsFromLineAfterToken(logLine, " : "))
    for line in aLogLineArray:
        similarLines = aLogLineArray
        similarLines.remove(line)
        similarLines = list(filter(lambda a: sameLength(line, a), similarLines))
        for similar in similarLines:
            finalVector.append(findParamValueAndReplaceIfSimilarLines(line, similar, 2))
    return set(finalVector)


#------------------Obvio que no hice tests al principio y ahora estoy dejando esto porque puedo------------------#
actualLogExtraction = """(h-checkout-v1-04) 2018-02-21 05:00:04,012 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)domain.util.timetracking.MeasureTimeAspect (ChasFacadeServiceImpl.java:28) : The Method chas.getRoomPacksV3 took 278 to run
(h-checkout-v1-04) 2018-02-21 05:00:04,022 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:39) : AbtestpriceWithoutSurprises does not apply so returns default branch
(h-checkout-v1-04) 2018-02-21 05:00:04,023 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:43) : AbtestDto was succesfully retrieved with value: AbTestDto{upperBound=50, abName=hurryUp, forceUpdate=false}
(h-checkout-v1-04) 2018-02-21 05:00:04,023 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:52) : abTestResult was found in cookies with value: AbTestResult{abTestName=hurryUp, abBranchWinner=branchB, apply=true, branchAWon=false, configurationsMap={banner=ab-HurryUp.ftl}}
(h-checkout-v1-04) 2018-02-21 05:00:04,024 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:43) : AbtestDto was succesfully retrieved with value: AbTestDto{upperBound=100, abName=chanchito, forceUpdate=false}
(h-checkout-v1-04) 2018-02-21 05:00:04,024 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:52) : abTestResult was found in cookies with value: AbTestResult{abTestName=chanchito, abBranchWinner=branchA, apply=true, branchAWon=true, configurationsMap={banner=ab-dummy.ftl}}
(h-checkout-v1-04) 2018-02-21 05:00:04,024 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:43) : AbtestDt was succesfully retrieved with value: AbTestDto{upperBound=50, abName=staypopup, forceUpdate=false}"""
result = parseLogText(actualLogExtraction)
print(result)



print("--------------------------------")
newLog = """5561 warn checkPermissions Missing write access to /usr/lib/node_modules/npm/node_modules/npmlog/node_modules
5562 warn checkPermissions Missing write access to /usr/lib/node_modules/npm/node_modules/osenv/node_modules
5563 warn checkPermissions Missing write access to /usr/lib/node_modules/npm/node_modules/read-package-json/node_modules/glob/node_modules/minimatch/node_modules/brace-expansion/node_modules
5564 Why God, why?"""
print(parseLogText(newLog))
