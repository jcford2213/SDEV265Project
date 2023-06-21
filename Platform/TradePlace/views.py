from django.shortcuts import render

def Dashboard(request):
    return render(request, 'TPTemplates/dashboard.html',{})

def Account(request):
    return render(request, 'TPTemplates/account.html',{})

def Ticker(request):
    return render(request, 'TPTemplates/ticker.html',{})

