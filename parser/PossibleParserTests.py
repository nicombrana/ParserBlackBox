import PossibleParser
import unittest


class TestPossibleParser(unittest.TestCase):

    def testGiven2LinesAStructuredLineIsCreated(self):
        aLine = "AbtestpriceWithoutSurprisesdoes not apply so returns default branch"
        anotherLine = "AbtestDto not apply so returns default branch"

        aStructuredLine = PossibleParser.findParamValueAndReplace(aLine, anotherLine, 2)

        self.assertEqual(aStructuredLine, "* not apply so returns default branch")


    def testGiven2SimilarLinesAstructuredLineIsCreated(self):
        aLine = "AbtestpriceWithoutSurprisesdoes not apply so returns default branch"
        anotherLine = "AbtestDto not apply so returns default branch"

        aStructuredLine = PossibleParser.findParamValueAndReplaceIfSimilarLines(aLine, anotherLine, 2)

        self.assertEqual(aStructuredLine, "* not apply so returns default branch")


    def testGiven2LinesNotSimilarNothingIsCreated(self):
        aLine = "AbtestDto was succesfully retrieved with value: AbTestDto{upperBound=50, abName=hurryUp, forceUpdate=false}"
        anotherLine = "The Method chas.getRoomPacksV3 took 278 to run"

        aStructuredLine = PossibleParser.findParamValueAndReplaceIfSimilarLines(aLine, anotherLine, 2)

        self.assertEquals(aStructuredLine, None)


    def testWhenTheLogLineHasColumnItTakesTheRestOfTheStringAsOnePart(self):
        aLine = "AbtestDto was succesfully retrieved with value: AbTestDto{upperBound=50, abName=hurryUp, forceUpdate=false}"
        anotherLine = "AbtestDto was succesfully retrieved with value: AbTestDto{upperBound=100, abName=chanchito, forceUpdate=false}"

        aStructuredLine = PossibleParser.findParamValueAndReplaceIfSimilarLines(aLine, anotherLine, 2)

        self.assertEqual(aStructuredLine, "AbtestDto was succesfully retrieved with value: *")


    def testWhenGivenACompleteLogLineTheInformationPartIsCorrectlyReturned(self):
        aCompleteLine = "(h-checkout-v1-04) 2018-02-21 05:00:04,023 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:43) : AbtestDto was succesfully retrieved with value: AbTestDto{upperBound=50, abName=hurryUp, forceUpdate=false}"
        informationLine = PossibleParser.removeTagsFromLineAfterToken(aCompleteLine, " : ")

        self.assertEqual(informationLine, "AbtestDto was succesfully retrieved with value: AbTestDto{upperBound=50, abName=hurryUp, forceUpdate=false}")


    def testGivenALogTextAnArrayOfStructuredLogLinesIsReturned(self):
        aLogText = """(h-checkout-v1-04) 2018-02-21 05:00:04,012 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)domain.util.timetracking.MeasureTimeAspect (ChasFacadeServiceImpl.java:28) : The Method chas.getRoomPacksV3 took 278 to run
        (h-checkout-v1-04) 2018-02-21 05:00:04,022 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:39) : AbtestpriceWithoutSurprises does not apply so returns default branch
        (h-checkout-v1-04) 2018-02-21 05:00:04,023 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:43) : AbtestDto was succesfully retrieved with value: AbTestDto{upperBound=50, abName=hurryUp, forceUpdate=false}
        (h-checkout-v1-04) 2018-02-21 05:00:04,023 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:52) : abTestResult was found in cookies with value: AbTestResult{abTestName=hurryUp, abBranchWinner=branchB, apply=true, branchAWon=false, configurationsMap={banner=ab-HurryUp.ftl}}
        (h-checkout-v1-04) 2018-02-21 05:00:04,024 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:43) : AbtestDto was succesfully retrieved with value: AbTestDto{upperBound=100, abName=chanchito, forceUpdate=false}
        (h-checkout-v1-04) 2018-02-21 05:00:04,024 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:52) : abTestResult was found in cookies with value: AbTestResult{abTestName=chanchito, abBranchWinner=branchA, apply=true, branchAWon=true, configurationsMap={banner=ab-dummy.ftl}}
        (h-checkout-v1-04) 2018-02-21 05:00:04,024 INFO [1DUv9FFU-hTeHfH50-h-checkout-v1-04-63160-CRl4uePK0m] [c1a09542-3493-409d-9edd-12a8ca98dce6] [http-9290-39] (...)hotels.domain.abtest.AbTestService (AbTestService.java:43) : AbtestDt was succesfully retrieved with value: AbTestDto{upperBound=50, abName=staypopup, forceUpdate=false}"""

        structuredLineArray = PossibleParser.parseLogText(aLogText)
        expectedStructuredLineArray = ['The Method chas.getRoomPacksV3 took 278 to run', 'AbtestpriceWithoutSurprises does not apply so returns default branch', '* was succesfully retrieved with value: *', 'abTestResult was found in cookies with value: *']

        self.assertEqual(structuredLineArray, expectedStructuredLineArray)
