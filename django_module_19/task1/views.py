from django.shortcuts import render, redirect, get_object_or_404
from .models import Buyer, Game
from django.http import HttpResponse

# Create your views here.
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
        return render(request, 'buy_game.html', context)