from enum import Enum
from dataclasses import dataclass
import numpy as np
import math
import plotly.graph_objects as go
from styles import degScoreProjectionStyle as plotsty

class CompletedDegreeError(Exception):
    pass

class MoreThanOneYearInProgressError(Exception):
    pass

class TargetGradeNotPossibleError(Exception):
    pass

class InvalidYesOrNoInputError(Exception):
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
    
    def _getTotalWeightOfRemainingYears(self):

        return 1 - 0.01 * np.sum([year.yearWeightPercentage for year in self.years])



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

        remainingYearWeights = self._getTotalWeightOfRemainingYears()

        yipProjectedScore, yipRemainingCredits, yipWeight = self._getYearInProgressScoreCreditsAndWeights()
    
        currentScore = self.calculateDegreeScore()

        requiredScore = (targetScore - currentScore*(1-remainingYearWeights) + yipWeight * yipProjectedScore * yipRemainingCredits / 120)/ \
        (yipWeight*yipRemainingCredits/120 + remainingYearWeights)

        
        requiredScore = math.ceil(requiredScore)

        if requiredScore > 100: 

            inp = input('This target score is impossible as you would need to average greater than 100, would you like to get a projections plot? y/n: ')
            if inp != 'y' and inp != 'n':
                raise InvalidYesOrNoInputError()
            
            if inp == 'n': 
                return
            
            self.getScoreProjectionsPlot()
            return
            
        
        return requiredScore
    
    def _calcFinalScore(self, remainingAverage):

        remainingYearWeights = self._getTotalWeightOfRemainingYears()

        yipProjectedScore, yipRemainingCredits, yipWeight = self._getYearInProgressScoreCreditsAndWeights()
    
        currentScore = self.calculateDegreeScore()

        finalScore = (1-remainingYearWeights)*currentScore - yipWeight*yipProjectedScore*yipRemainingCredits/120 \
            + remainingAverage * (yipWeight*yipRemainingCredits/120 + remainingYearWeights)

        return math.floor(finalScore)

    def getScoreProjectionsPlot(self, start=40, stop=100, increment = 5):

        if stop > 100: 
            raise TargetGradeNotPossibleError()
        
        averages = list(np.arange(start, stop+increment, increment))
        finalScores = [self._calcFinalScore(avg) for avg in averages]

        fig = go.Figure()
        fig.update_layout(**plotsty['layout'])
        fig.update_layout(**plotsty['axes'])
        fig.update_layout(
        title_text='<b>DEGREE SCORE PROJECTION FROM CURRENT SCORE {}</b>'.format(self.calculateDegreeScore()), 
        xaxis_title = 'Average Score For Remainder Of Degree', 
        yaxis_title = 'Final Degree Score'
        )

        fig.add_trace(go.Scatter(x=averages, y=finalScores, marker_color='#aa8c2c'))
        fig.show()








        
        



    