"""
Views file implements the render function to render templates and return HTTP responses.
Index returns a rendered template for a welcome message.
About returns a rendered template for the about page.
"""
from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'MoneyParce'
    return render(request, 'home/index.html', {
        'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {
        'template_data': template_data})