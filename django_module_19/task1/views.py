from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import *
from .forms import UserRegister


# Create your views here.
def news(request):
    new = News.objects.all().order_by('-date')
    paginator = Paginator(new, 3)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    return render(request, 'paginator/news.html', {'news': news})


def platform(request):
    return render(request, 'fourth_task/platform.html')


def games(request):
    games = Game.objects.all()
    context = {
        'games': games,
    }
    return render(request, 'fourth_task/games.html', context)


def cart(request):
    title = 'Cart'
    context = {
        'title': title,
    }
    return render(request, "fourth_task/cart.html")


def sign_up_by_django(request):
    info = {}
    form = UserRegister(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            buyers = Buyer.objects.values_list('name', flat=True)

            if username in buyers:
                info['error'] = 'Пользователь уже существует'
            elif password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif age < 18:
                info['error'] = 'Вы должны быть старше 18'
            else:
                Buyer.objects.create(name=username, age=age, balance=1000)
                info['message'] = f'Приветствуем, {username}!'

        info['form'] = form

        return render(request, 'fifth_task/registration_page.html', info)


def sign_up_by_html(request):
    info = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age'))

        buyers = Buyer.objects.values_list('name', flat=True)

        if username in buyers:
            info['error'] = 'Пользователь уже существует'
        elif password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        elif age < 18:
            info['error'] = 'Вы должны быть старше 18'
        else:
            Buyer.objects.create(name=username, age=age, balance=1000)
            info['message'] = f'Приветствуем, {username}!'

    return render(request, 'fifth_task/registration_page.html', context=info)


def buy_game(request, game_id):
    """
    Представление для покупки игры.
    Проверяет возраст покупателя и достаточность баланса.
    """
    game = get_object_or_404(Game, pk=game_id)
    buyer = get_object_or_404(Buyer, name=request.user.username) # Предполагается аутентификация пользователя

    if request.method == 'POST':
        if buyer.age >= 18 or not game.age_limited:  # Проверка возраста
            if buyer.balance >= game.cost: # Проверка баланса
                buyer.balance -= game.cost
                buyer.save()
                game.buyers.add(buyer)
                return HttpResponse("Игра успешно куплена!")  # Можно сделать более красивое сообщение
            else:
                return HttpResponse("Недостаточно средств на балансе.")
        else:
            return HttpResponse("Вы слишком молоды для этой игры.")
    else:
        context = {'game': game, 'buyer': buyer}  #  Передаем данные в шаблон
        return render(request, 'task_1/buy_game.html', context)

