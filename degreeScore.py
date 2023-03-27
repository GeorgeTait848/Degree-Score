from enum import Enum
from dataclasses import dataclass
import numpy as np


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

        if totalCredits < 120:
            print('Note, the modules you have given are do not equal 120 so this is a projected score.')

        return 100*achievedCredits/totalCredits



    

def main():
    
    year3Modules = [
        Module('Nuclear Physics', 10, [ModuleAssessment(Assessment.EXAM, 100, 67)]), 
        Module('Introduction to Differential Geometry', 10, [ModuleAssessment(Assessment.EXAM, 100, 98)]),
        Module('Introduction to Dynamical Systems', 10, [ModuleAssessment(Assessment.EXAM, 100, 69)]), 
        Module('Research Methods in Physics', 15, [ModuleAssessment(Assessment.COURSEWORK, 50, 74), ModuleAssessment(Assessment.COURSEWORK, 50, 67)]), 
    ]

    year3 = UniversityYear(
        yearNumber = 3, 
        yearWeightPercentage = 40,
        modules=year3Modules
        )

    print(year3.calculateYearScorePercentage())



if __name__ == "__main__":
    main()