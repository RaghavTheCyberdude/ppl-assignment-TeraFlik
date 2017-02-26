from django import forms
from .models import *
from .constants import *

class GetNumberForm(forms.Form):
	number = forms.IntegerField(max_value=200)

class GetGiftNumberForm(forms.Form):
	giftType = forms.ChoiceField(choices=giftTypes, required=True)
	number = forms.IntegerField(max_value=200)

class BoyForm(forms.ModelForm):
	boyType = forms.ChoiceField(choices=committedBoyTypes, required=True)

	class Meta:
		model = Boy
		fields = ('name', 'attractiveness', 'intelligenceLevel', 'isCommitted', 'budget', 'attractionRequirement', 'boyType')
		help_texts = {
			'attractiveness': 'Between 1 to 10',
			'intelligenceLevel': 'Between 1 to 10',
			'attractionRequirement': 'Between 1 to 10',
		}

class GirlForm(forms.ModelForm):
	girlType = forms.ChoiceField(choices=committedGirlTypes, required=True)

	class Meta:
		model = Girl
		fields = ('name', 'attractiveness', 'intelligenceLevel', 'isCommitted', 'maintenanceBudget', 'datingCriteria', 'girlType')
		help_texts = {
			'attractiveness': 'Between 1 to 10',
			'intelligenceLevel': 'Between 1 to 10',
		}

class EssentialGiftForm(forms.ModelForm):
	class Meta:
		model = EssentialGift
		fields = ('price', 'value')

class LuxuryGiftForm(forms.ModelForm):
	class Meta:
		model = LuxuryGift
		fields = ('price', 'value', 'luxuryRating', 'difficultyToObtain')

class UtilityGiftForm(forms.ModelForm):
	utilityClass = forms.ChoiceField(choices=utilityClasses, required=True)
	
	class Meta:
		model = UtilityGift
		fields = ('price', 'value', 'utilityValue', 'utilityClass')

class RelationForm(forms.ModelForm):
	class Meta:
		model = Relation
		fields = ('boy', 'girl', 'commitOn', 'breakupOn')