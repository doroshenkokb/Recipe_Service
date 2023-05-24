from io import BytesIO

from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def download_pdf(request, ingredients):
    """Функция для отправки списка покупок в pdf"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'inline; filename="shopping_list.pdf"'
    )

    buffer = BytesIO()
    page = canvas.Canvas(buffer)

    pdfmetrics.registerFont(
        TTFont(
            'Roboto-Regular',
            'static/fonts/Roboto-Regular.ttf', 
            'UTF-8'
        )
    )
    page.setFont('Roboto-Regular', size=24)
    page.drawString(150, 800, 'Рецепты с сайта Foodgram')
    page.setFont('Roboto-Regular', size=20)
    page.drawString(130, 750, 'Список ингредиентов для рецептов')
    page.setFont('Roboto-Regular', size=16)
    height = 700
    for ingredient_name, measurement_unit, amount in ingredients:
        page.drawString(
            50, 
            height, 
            f'• {ingredient_name} - {amount} '
            f'{measurement_unit}'
        )
        height -= 20

    page.showPage()
    page.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
