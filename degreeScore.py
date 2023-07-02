from enum import Enum
from dataclasses import dataclass
import numpy as np
import math

class CompletedDegreeError(Exception):
    pass

class MoreThanOneYearInProgressError(Exception):
    pass

class TargetGradeNotPossibleError(Exception):
    pass


class Assessment(Enum):

    COURSEWORK = "coursework"
    EXAM = "exam"



@dataclass
class ModuleAssessment:

    assessment: Assessment
    weightPercentage: int
    scorePercentage: int


@dataclass
class Module:
    name: str
    credits: int
    assessments: list[ModuleAssessment]

    def getAssessmentScoresAndWeights(self):

        scores = [float(assessment.scorePercentage) for assessment in self.assessments]
        weights = [float(assessment.weightPercentage)/100 for assessment in self.assessments] 

        return scores, weights


    def calculateModuleScorePercentage(self) -> int:

        scores, weights = self.getAssessmentScoresAndWeights()
        return  np.average(scores, weights=weights)


                
@dataclass
class UniversityYear: 

    yearNumber: int
    yearWeightPercentage: int
    modules: list[Module]
    

    def calculateTotalCredits(self):

        totalCredits = 0

        for module in self.modules:
            totalCredits += module.credits

        return totalCredits


    def calculateAchievedCredits(self):

        achievedCreditsPerModule = [module.calculateModuleScorePercentage()*module.credits/100 for module in self.modules]
        return np.sum(achievedCreditsPerModule)



    def calculateYearScorePercentage(self):

        achievedCredits = self.calculateAchievedCredits()
        totalCredits = self.calculateTotalCredits()

        return 100*achievedCredits/totalCredits


@dataclass 
class Degree:

    years: list[UniversityYear]

    def calculateDegreeScore(self) -> int:
        
        weights = [year.yearWeightPercentage/100 for year in self.years]
        scores = [year.calculateYearScorePercentage() for year in self.years]

        return round(np.average(scores, weights=weights))

    def _getYearInProgress(self):

        yearsInProgress = list(filter(lambda year: year.calculateTotalCredits() < 120, self.years))

        if yearsInProgress == []:
            return None
        
        if len(yearsInProgress) > 1:
            raise MoreThanOneYearInProgressError()
        
        return yearsInProgress[0]

    def _getYearInProgressScoreCreditsAndWeights(self):

        yearInProgress = self._getYearInProgress()

        if yearInProgress == None:
            yipRemainingCredits, yipWeight, yipScore = 0,0,0

        else: 
            yipRemainingCredits = 120 - yearInProgress.calculateTotalCredits() 
            yipWeight = yearInProgress.yearWeightPercentage/100
            yipScore = yearInProgress.calculateYearScorePercentage()
        
        return yipScore, yipRemainingCredits, yipWeight



    def calculateRequiredAverageForTargetScore(self, targetScore: int): 

        '''Calculated via the equation: 
        
        A_R = (S_T - (1  - W_R)*S_P + W_1*S_1*r/120)/(W_1*r/120 + W_R)

        Where:
        A_R is the required average to achieve target score S_T.
        W_R is the total weight percentage of any years that are yet to be completed
        S_P is the current projected degree score.
        W_1,S_1 are the weight, projected score of the current year, respectively.
        r is the remanining credits of the year in progress
        W_R is the total weight of uncompleted years. 
        
        '''

        remainingYearWeights = 1 - 0.01 * np.sum([year.yearWeightPercentage for year in self.years])
        yearsInProgress = self._getYearInProgress()

        yipProjectedScore, yipRemainingCredits, yipWeight = self._getYearInProgressScoreCreditsWeights()
    
        currentScore = self.calculateDegreeScore()

        requiredScore = (targetScore - currentScore*(1-remainingYearWeights) + yipWeight * yipProjectedScore * yipRemainingCredits / 120)/ \
        (yipWeight*yipRemainingCredits/120 + remainingYearWeights)

        
        requiredScore = math.ceil(requiredScore)

        if requiredScore > 100: 
            raise TargetGradeNotPossibleError()
        
        return requiredScore


        
        



    