from degreeScore import *


def main():

    year2Modules = [
        Module('', 10, [ModuleAssessment(Assessment.COURSEWORK, 100, 62)]), 
        Module('', 20, [ModuleAssessment(Assessment.COURSEWORK, 100, 63)]), 
        Module('', 10, [ModuleAssessment(Assessment.COURSEWORK, 100, 62)]),
        Module('', 20, [ModuleAssessment(Assessment.COURSEWORK, 100, 67)]), 
        Module('', 10, [ModuleAssessment(Assessment.COURSEWORK, 100, 58)]), 
        Module('', 10, [ModuleAssessment(Assessment.COURSEWORK, 100, 55)]), 
        Module('', 10, [ModuleAssessment(Assessment.EXAM, 100, 62)]), 
        Module('', 10, [ModuleAssessment(Assessment.EXAM, 100, 60)]), 
        Module('', 20, [ModuleAssessment(Assessment.COURSEWORK, 50, 65), ModuleAssessment(Assessment.EXAM, 50, 60)])
    ]

    year3Modules = [
        Module('', 10, [ModuleAssessment(Assessment.COURSEWORK, 100, 79)]), 
        Module('', 20, [ModuleAssessment(Assessment.EXAM, 40, 72), ModuleAssessment(Assessment.COURSEWORK, 60, 77)]),
    ]

    year2 = UniversityYear(
        yearNumber = 2,
        yearWeightPercentage= 40,
        modules= year2Modules
        )

    year3 = UniversityYear(
        yearNumber = 3, 
        yearWeightPercentage = 60,
        modules=year3Modules
        )

    myDegree = Degree(years=[year2, year3])
    print("Third Year Score: ",year3.calculateYearScorePercentage())
    print("Degree Score: ", myDegree.calculateDegreeScore())
    print("Required Average To Achieve 1st: ", myDegree.calculateRequiredAverageForTargetScore(70))
    myDegree.getScoreProjectionsPlot()


if __name__ == "__main__":
    main()