from degreeScore import *


def main():

    year2Modules = [
        Module('Advanced Computational Modelling and Simulation', 20, [ModuleAssessment(Assessment.COURSEWORK, 100, 85)]), 
        Module('Complex Analysis', 10, [ModuleAssessment(Assessment.EXAM, 100, 88)]), 
        Module('Core Physics III: Quantum Physics', 20, [ModuleAssessment(Assessment.COURSEWORK, 100, 70)]),
        Module('Core Physics IIV: Statistical and Solid State Physics', 20, [ModuleAssessment(Assessment.COURSEWORK, 100, 70)]), 
        Module('Mathematics for Physics II', 20, [ModuleAssessment(Assessment.COURSEWORK, 30, 94), ModuleAssessment(Assessment.EXAM, 70, 94)]), 
        Module('Physics Laboratory', 20, [ModuleAssessment(Assessment.COURSEWORK, 100, 61)]), 
        Module('Probability Theory', 10, [ModuleAssessment(Assessment.EXAM, 100, 55)])
    ]

    year3Modules = [
        Module('Nuclear Physics', 10, [ModuleAssessment(Assessment.EXAM, 100, 67)]), 
        Module('Introduction to Differential Geometry', 10, [ModuleAssessment(Assessment.EXAM, 100, 98)]),
        Module('Introduction to Dynamical Systems', 10, [ModuleAssessment(Assessment.EXAM, 100, 69)]), 
        Module('Research Methods in Physics', 30, [ModuleAssessment(Assessment.COURSEWORK, 25, 74), ModuleAssessment(Assessment.COURSEWORK, 25, 67),ModuleAssessment(Assessment.EXAM, 50, 64)]),
        Module('High Energy and Plasma Physics', 10, [ModuleAssessment(Assessment.EXAM, 100, 95)]), 
        Module('Linear Differential Equations', 10, [ModuleAssessment(Assessment.EXAM, 100, 75)]), 
        Module('Vibrations and Waves', 10, [ModuleAssessment(Assessment.EXAM, 100, 85)]), 
        Module('Group Project', 30, [ModuleAssessment(Assessment.COURSEWORK, 100, 66)])
    ]

    year4Modules = [
        Module('Final Year Project', 60, [ModuleAssessment(Assessment.COURSEWORK, 100, 76)]), 
        Module('Advanced Quantum Mechanics', 15, [ModuleAssessment(Assessment.EXAM, 100, 95)]), 
        Module('Mathematical Modelling I', 15, [ModuleAssessment(Assessment.COURSEWORK, 40, 78), ModuleAssessment(Assessment.COURSEWORK, 60, 73)])
    ]

    year2 = UniversityYear(
        yearNumber = 2,
        yearWeightPercentage= 20,
        modules= year2Modules
        )

    year3 = UniversityYear(
        yearNumber = 3, 
        yearWeightPercentage = 40,
        modules=year3Modules
        )

    year4 = UniversityYear(yearNumber=4, yearWeightPercentage=40, modules=year4Modules)
    print(year4.calculateYearScorePercentage())

    myDegree = Degree(years=[year2, year3])

    print(myDegree.calculateDegreeScore())
    print(myDegree.calculateRequiredAverageForTargetScore(77))
    myDegree.getScoreProjectionsPlot()


if __name__ == "__main__":
    main()