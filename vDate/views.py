from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
# Create your views here.

def newBoy(request):
	if request.method == 'POST':
		form = BoyForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('boys.html')
	else:
		form = PostForm()
	return render(request, 'new_boy.html', {'form': form})

def newGirl(request):
	if request.method == 'POST':
		form = GirlForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('girl.html')
	else:
		form = PostForm()
	return render(request, 'new_girl.html', {'form': form})