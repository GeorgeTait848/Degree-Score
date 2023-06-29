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
        
        weights = [year.yearWeightPercentage for year in self.years]
        scores = [year.calculateYearScorePercentage() for year in self.years]

        return round(np.average(scores, weights=weights))

    def calculateRequiredAverageForTargetScore(self, targetScore: int): 

        '''Calculated via the equation: 
        
        t = (x - (1  -W_R)*S_P + W_1*S_1*r/120)/(W_1*r/120 + W_R)

        Where:
        x is the target score
        t is the required average to acquire this score
        S_P is the current degree score, projected.
        The subscript 1 refers to any year in progress, if there is one. 
        r is the remanining credits of the year in progress
        W_R is the total weight percentage of any years that are yet to be completed
        '''

        remainingYearWeights = 1 - 0.01 * np.sum([year.yearWeightPercentage for year in self.years])
        yearsInProgress = list(filter(lambda year: year.calculateTotalCredits() < 120, self.years))

        if remainingYearWeights == 0 and yearsInProgress == []:
            raise CompletedDegreeError()

        if len(yearsInProgress) > 1: 
            raise MoreThanOneYearInProgressError()
        

        if yearsInProgress == []:
            yipRemainingCredits, yipWeight, yipScore = 0,0,0

        else: 
            yearInProgress = yearsInProgress[0]
            yipRemainingCredits = 120 - yearInProgress.calculateTotalCredits() 
            yipWeight = yearInProgress.yearWeightPercentage/100
            yipScore = yearInProgress.calculateYearScorePercentage()
        
        currentScore = self.calculateDegreeScore()

        requiredScore = (targetScore - currentScore*(1-remainingYearWeights) + yipWeight * yipScore * yipRemainingCredits / 120)/ \
        (yipWeight*yipRemainingCredits/120 + remainingYearWeights)

        
        requiredScore = math.ceil(requiredScore)

        if requiredScore > 100: 
            raise TargetGradeNotPossibleError()
        
        return requiredScore


        
        



    