from django import forms
from .models import *
from .choices import *

class BoyForm(forms.ModelForm):
	class Meta:
		model = Boy
		fields = ('name', 'attractiveness', 'intelligenceLevel', 'budget', 'attractionRequirement', 'boyType')
		widgets = {
			'boyType': forms.ChoiceField(choices=committedBoyTypes, widget=forms.RadioSelect, required=True),
			}

class GirlForm(forms.ModelForm):
	class Meta:
		model = Girl
		fields = ('name', 'attractiveness', 'intelligenceLevel', 'maintenanceBudget', 'datingCriteria', 'girlType')
		widgets = {
			'girlType': forms.ChoiceField(choices=committedGirlTypes, widget=forms.RadioSelect, required=True),
			}

class EssentialGiftForm(forms.ModelForm):
	class Meta:
		model = Gift
		fields = ('price', 'value')

class LuxuryGiftForm(forms.ModelForm):
	class Meta:
		model = Gift
		fields = ('price', 'value', 'luxuryRating', 'difficultyToObtain')

class UtilityGiftForm(forms.ModelForm):
	class Meta:
		model = Gift
		fields = ('price', 'value', 'utilityValue', 'utilityClass')