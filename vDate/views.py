from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
from .forms import *
from vDate.new import *

"""
These views serve all the data to the front-end templates.
"""

def home(request):
	exchangesList = Exchange.objects.all()
	happyCouples = Relation.objects.all().order_by('-happiness')
	compatibleCouples = Relation.objects.all().order_by('-compatibility')
	return render(request, 'vDate/Q2.html', {'happyCouples': happyCouples, 'compatibleCouples': compatibleCouples})

def boys(request):
	"""
	Prints list of all boys.
	Using POST form recieves the number of random entries to generate for the boy class.
	Can create a custom Boy using another POST form.
	"""
	manual = False	
	boyForm = BoyForm(prefix='manual')
	if request.method == 'POST':
		boyForm = BoyForm(request.POST, prefix='manual')
		if boyForm.is_valid():
			boyForm.save()
			manual = True
		numForm = GetNumberForm(request.POST, prefix='auto')
		if not manual and numForm.is_valid():
			number = numForm.cleaned_data['number']
			if isinstance(number, int):
				for i in range(number):
					newRandomBoy()
			boyForm = BoyForm(prefix='manual')
	numForm = GetNumberForm(prefix='auto')
	boysList = Boy.objects.all().order_by('name')
	return render(request, 'vDate/boys.html', {'boysList': boysList, 'boyForm': boyForm, 'getNumberForm': numForm})

def girls(request):
	"""
	Prints list of all girls.
	Using POST form recieves the number of random entries to generate for the girl class.
	Can create a custom Girl using another POST form.
	"""
	manual = False	
	girlForm = GirlForm(prefix='manual')
	if request.method == 'POST':
		girlForm = GirlForm(request.POST, prefix='manual')
		if girlForm.is_valid():
			girlForm.save()
			manual = True
		numForm = GetNumberForm(request.POST, prefix='auto')
		if not manual and numForm.is_valid():
			number = numForm.cleaned_data['number']
			for i in range(number):
				newRandomGirl()
			girlForm = GirlForm(prefix='manual')
	numForm = GetNumberForm(prefix='auto')
	girlsList = Girl.objects.all().order_by('name')
	return render(request, 'vDate/girls.html', {'girlsList': girlsList, 'girlForm': girlForm, 'getNumberForm': numForm})


def gifts(request):
	"""
	Prints list of all Gifts- Essential, Luxury and Utility Gifts.
	Using POST form recieves the number of random entries to generate for the a particular gift class.
	Can create a custom Gifts of required type using 3 other POST forms.
	"""
	handled = False
	giftNumForm = GetGiftNumberForm(prefix='auto')
	essentialGiftForm = EssentialGiftForm(prefix='essentialGift')
	luxuryGiftForm = LuxuryGiftForm(prefix='luxuryGift')
	utilityGiftForm = UtilityGiftForm(prefix='utilityGift')
	if request.method == 'POST':
		giftNumForm = GetGiftNumberForm(request.POST, prefix='auto')
		if giftNumForm.is_valid():
			handled = True
			giftType = giftNumForm.cleaned_data['giftType']
			number = giftNumForm.cleaned_data['number']
			for i in range(number):
				if giftType == '1':
					newEssentialGift()
				elif giftType == '2':
					newLuxuryGift()
				elif giftType == '3':
					newUtilityGift()
		if not handled:
			essentialGiftForm = EssentialGiftForm(request.POST, prefix='essentialGift')
			if essentialGiftForm.is_valid():
				handled = True
				essentialGiftForm.save()
		if not handled:
			luxuryGiftForm = LuxuryGiftForm(request.POST, prefix='luxuryGift')
			if luxuryGiftForm.is_valid():
				handled = True
				luxuryGiftForm.save()
		if not handled:	
			utilityGiftForm = UtilityGiftForm(request.POST, prefix='utilityGift')
			if utilityGiftForm.is_valid():
				utilityGiftForm.save()
				handled = True
	if handled:
		giftNumForm = GetGiftNumberForm(prefix='auto')
		essentialGiftForm = EssentialGiftForm(prefix='essentialGift')
		luxuryGiftForm = LuxuryGiftForm(prefix='luxuryGift')
		utilityGiftForm = UtilityGiftForm(prefix='utilityGift')
	essentialGiftsList = EssentialGift.objects.all().order_by('price')
	luxuryGiftsList = LuxuryGift.objects.all().order_by('price')
	utilityGiftsList = UtilityGift.objects.all().order_by('price')
	return render(request, 'vDate/gifts.html',{
		'essentialGiftsList': essentialGiftsList,
		'luxuryGiftsList': luxuryGiftsList,
		'utilityGiftsList': utilityGiftsList,
		'essentialGiftForm': essentialGiftForm,
		'luxuryGiftForm': luxuryGiftForm,
		'utilityGiftForm': utilityGiftForm,
		'giftNumberForm': giftNumForm
		})

def relations(request):
	"""
	Prints list of all the relations currently existing.
	Using POST form recieves the number of random relations to create subject to availability of suitable matches.
	"""
	relationsList = Relation.objects.all()
	exchangesList = Exchange.objects.all()
	handled = False
	if exchangesList.exists():
		status = True
	else:
		status = False
	numForm = GetNumberForm()
	if request.method == 'POST':
		numForm = GetNumberForm(request.POST)
		if numForm.is_valid():
			handled = True
			number = numForm.cleaned_data['number']
			girlCount = Girl.objects.filter(isCommitted=False).count()
			if number > girlCount:
				messages.error(request, "Not enough single girls!")
			else:
				girlList = Girl.objects.filter(isCommitted=False)[:number]	
				for girl in girlList:
					findMatch(girl)
		elif not handled and request.POST.get('type') == 'gifting':
			handled = True
			if status:
				messages.error(request, "Gifting Already Performed!")
			else:
				for relation in Relation.objects.all():
					performGifting(relation)
					relation.findHappiness()
	if handled:
		numForm = GetNumberForm()
	return render(request, 'vDate/relations.html', {
		'relationsList': relationsList,
		'exchangesList': exchangesList,
		'getNumberForm': numForm,
		'status': status,
		})

def deleteEntries(request):
	"""
	Purpose of this View is to serve the "Delete all" button at the end of all pages to get rid of the records and insert new records to database.
	"""
	if request.method == 'POST':
		if request.POST.get('type') == 'boys':
			Boy.objects.all().delete()
			return HttpResponseRedirect(reverse('boys'))
		elif request.POST.get('type') == 'girls':
			Girl.objects.all().delete()
			return HttpResponseRedirect(reverse('girls'))
		elif request.POST.get('type') == 'gifts':
			EssentialGift.objects.all().delete()
			LuxuryGift.objects.all().delete()
			UtilityGift.objects.all().delete()
			return HttpResponseRedirect(reverse('gifts'))
		elif request.POST.get('type') == 'relations':
			for relation in Relation.objects.all():
				relation.breakup()
			return HttpResponseRedirect(reverse('relations'))
	return HttpResponseRedirect(reverse('home'))
