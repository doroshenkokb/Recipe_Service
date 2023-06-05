from io import BytesIO

from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from users.models import Follow


def download_pdf(*ingredients_pages):
    """Функция для отправки списка покупок в pdf"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="shopping_list.pdf"'
    buffer = BytesIO()
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Arial', 'data/arial.ttf', 'UTF-8'))
    page.setFont('Arial', size=20)
    page.drawString(130, 750, 'Список ингредиентов для рецептов')
    page.setFont('Arial', size=16)
    initial_height = 700
    max_ingredients_per_page = 30
    ingredients_count = 0

    for ingredients_cart in ingredients_pages:
        for index, ingredient_data in enumerate(ingredients_cart, start=1):
            ing_name, unit, amount = ingredient_data
            ingredient_string = f'{index}. {ing_name} - {amount} {unit}'
            height = initial_height - (ingredients_count % max_ingredients_per_page) * 20
            page.drawString(50, height, ingredient_string)
            ingredients_count += 1
            if ingredients_count % max_ingredients_per_page == 0:
                page.showPage()
                page.setFont('Arial', size=16)

    page.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def check_anonymous_return_bool(self, obj, model):
    """
    Проверяем существует ли запрос, анонимен ли пользователь
    и возвращаем булево значение на основе указанного поля модели.
    """
    request = self.context.get('request')
    if not request or request.user.is_anonymous:
        return False
    if model == Follow:
        return model.objects.filter(user=request.user, author=obj.id).exists()
    return model.objects.filter(recipe=obj, user=request.user).exists()
