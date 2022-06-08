from django.http import HttpResponse
from django.shortcuts import render
from .forms import FeedbackForm
from . import canteenbot, sssbot ,clginfobot, librarybot, placementbot, sportsbot, stringerrorforgiver
import sqlite3

# Create your views here.

def index(request):
    context = {}
    return render(request, "index.html")


def services(request):
    context = {}
    return render(request, "services.html")


def about(request):
    context = {}
    return render(request, "about.html")


def contact(request):
    context = {}
    return render(request, "contact.html")


def college(request):
    context = {}
    def query_data(inp):
        query = f"SELECT staff_details,staff_expyr,staff_doj,staff_room,staff_qualification,staff_handle_subs,year,class,staff_cont_num,staff_name,class_location,ucen_common_details,bus_cons_details,mark_sheet_ver,academic_details FROM clg_info_details WHERE clg_info_tag ='{inp}'" 
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        conn.close()
        # print(results)
        return results
    def chat(msg):
        rresponse = clginfobot.response(msg) 
        return rresponse
    def img():
        image = clginfobot.response.contextimg
        return image

    if request.method == 'POST':
        msg = request.POST.get('input', '')
        context['query'] = msg
        context['chatresponse'] = chat(msg)
        context['imgresponse'] = img()
        tag = clginfobot.response.tagg
        context['dataresponse'] = query_data(tag)        
    return render(request, "clginfobot.html",context)


def placement(request):
    context = {}
    def query_data(inp):
        query = f"SELECT details,company,Atos2021_2022,officer,internship2021,tcs FROM placement_details WHERE placement_details_tag ='{inp}'" 
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        conn.close()
        # print(results)
        return results
    def chat(msg):
        rresponse = placementbot.response(msg) 
        return rresponse
    def img():
        image = placementbot.response.contextimg
        return image

    if request.method == 'POST':
        msg = request.POST.get('input', '')
        context['query'] = msg
        context['chatresponse'] = chat(msg)
        context['imgresponse'] = img()
        tag = placementbot.response.tagg
        context['dataresponse'] = query_data(tag)
    return render(request, "placementbot.html",context)


def library(request):
    context = {}
    def query_data(inp):
        query = f"SELECT details1 FROM library_details WHERE library_details_tag ='{inp}'" 
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        conn.close()
        # print(results)
        return results
    
    def img():
        image = canteenbot.response.contextimg
        return image

    def chat(msg):
        rresponse = librarybot.response(msg) 
        return rresponse
    

    if request.method == 'POST':
        msg = request.POST.get('input', '')
        context['query'] = msg
        context['chatresponse'] = chat(msg)
        tag = librarybot.response.tagg
        context['dataresponse'] = query_data(tag)
        context['imgresponse'] = img()
    return render(request, "librarybot.html",context)


def booksearch(request):
    context = {}
    def findingbook(inp):
        query = f"SELECT books,author,year,book_availability FROM library WHERE books ='{inp}'" 
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        conn.close()
        return results

    if request.method == 'POST':
        book = request.POST.get('input', '')
        correct_string = stringerrorforgiver.forgive_bookname(book)
        context['query'] = book
        context['details'] = findingbook(correct_string)
    return render(request, "booksearch.html",context)


def authorsearch(request):
    context = {}
    def findingbook(inp):
        query = f"SELECT books,author,year,book_availability FROM library WHERE author ='{inp}'" 
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        conn.close()
        return results

    if request.method == 'POST':
        author = request.POST.get('input', '')
        correct_string = stringerrorforgiver.forgive_authorname(author)
        context['query'] = author
        context['details'] = findingbook(correct_string)

    return render(request, "authorsearch.html",context)


def sss(request):
    context = {}
    def chat(msg):
        rresponse = sssbot.response(msg) 
        return rresponse

    if request.method == 'POST':
        msg = request.POST.get('input', '')
        context['query'] = msg
        context['chatresponse'] = chat(msg)
    return render(request, "sssbot.html",context)


def canteen(request):
    context = {}
    def chat(msg):
        rresponse = canteenbot.response(msg) 
        return rresponse
    def img():
        image = canteenbot.response.contextimg
        return image

    if request.method == 'POST':
        msg = request.POST.get('input', '')
        context['query'] = msg
        context['chatresponse'] = chat(msg)
        context['imgresponse'] = img()
    return render(request, "canteenbot.html",context)


def sports(request):
    context = {}
    def query_data(inp):
        
        query = f"SELECT time_of_game,game_list,captain_of_game,staff,grounds,tournament_timing,overview FROM sports_details WHERE game_details_tag ='{inp}'" 
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        conn.close()

        print(results)
        return results
    def chat(msg):
        rresponse = sportsbot.response(msg) 
        return rresponse
    def img():
        image = sportsbot.response.contextimg
        return image
        
    if request.method == 'POST':
        msg = request.POST.get('input', '')
        context['query'] = msg
        context['chatresponse'] = chat(msg)
        context['imgresponse'] = img()
        tag = sportsbot.response.tagg

        context['dataresponse'] = query_data(tag)

    return render(request, "sportsbot.html",context)


def feedback_form(request):

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, 'form/thanks.html')
    else:
        form = FeedbackForm()
    context = {'form': form}
    return render(request, 'form/feedback_form.html', {'form': form})