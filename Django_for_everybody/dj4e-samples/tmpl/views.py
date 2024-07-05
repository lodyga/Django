from django.shortcuts import render
from django.views import View

# Create your views here.


def simple(request):
    return render(request, 'tmpl/simple.html')


def guess(request):
    context = {'zap': '42'}
    return render(request, 'tmpl/guess.html', context)


def special(request):
    context = {
        'zap': '42',
        'txt': '<b>bold</b>'
    }
    return render(request, 'tmpl/special.html', context)


def loop(request):
    f = ['Apple', 'Orange', 'Banana', 'Lychee']
    n = ['peanut', 'cashew']
    context = {
        'fruits': f,
        'nuts': n,
        'zap': '42'
    }
    return render(request, 'tmpl/loop.html', context)


def cond(request):
    context = {'guess': '42'}
    return render(request, 'tmpl/cond.html', context)


def nested(request):
    context = {'outer': {'inner': '42'}}
    return render(request, 'tmpl/nested.html', context)

# Call this with a parameter number


class GameView(View):
    def get(self, request, guess):
        context = {'guess': int(guess)}
        return render(request, 'tmpl/cond.html', context)

# Using inheritance (extend)


class Game2View(View):
    def get(self, request, guess):
        context = {'guess': int(guess)}
        return render(request, 'tmpl/cond2.html', context)
