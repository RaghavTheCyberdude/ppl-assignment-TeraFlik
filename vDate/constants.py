"""
This file contains the list of all the choices and constants used all over the program.
To include simply use: from .constants import *
"""

datingCriteriaChoices = (
	(1, "Most Attractive"),
	(2, "Most Rich"),
	(3, "Most Intelligent")
)

committedGirlTypes = (
	(1, "The Choosy"),
	(2, "The Normal"),
	(3, "The Desperate")
)

committedBoyTypes = (
	(1, "The Miser"),
	(2, "The Generous"),
	(3, "The Geek")
)

giftTypes = (
	(1, "Essential Gift"),
	(2, "Luxury Gift"),
	(3, "Utility Gift")
)

utilityClasses = (
	(1, "Health"),
	(2, "Home"),
	(3, "Kitchen"),
	(4, "Sanitation"),
	(5, "Stationary")
)

attractionMin = 1
attractionMode = 7
attractionMax = 10

intelligenceMin = 1
intelligenceMode = 7
intelligenceMax = 10

maintenanceBudgetMin = 500
maintenanceBudgetMode = 5000
maintenanceBudgetMax = 50000

budgetMin = 500
budgetMode = 5000
budgetMax = 75000

giftMin = 20
giftMode = 200
giftMax = 1000

luxuryGiftMin = 1000
luxuryGiftMode = 5000
luxuryGiftMax = 50000

ratingMin = 1
ratingMax = 5
ratingMode = 2