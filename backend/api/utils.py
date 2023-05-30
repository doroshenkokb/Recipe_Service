import io

from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def download_pdf(ingredients_cart):
    """Функция для отправки списка покупок в pdf"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        "attachment; filename='shopping_cart.pdf'"
    )
    pdfmetrics.registerFont(TTFont('Arial', 'data/arial.ttf', 'UTF-8'))
    buffer = io.BytesIO()
    pdf_file = canvas.Canvas(buffer)
    pdf_file.setFont('Arial', 24)
    pdf_file.drawString(200, 800, 'Список покупок.')
    pdf_file.setFont('Arial', 14)
    page_height = pdf_file._pagesize[1]
    max_items_per_page = 22
    for number, ingredient in enumerate(ingredients_cart, start=1):
        from_bottom = page_height - (number % max_items_per_page) * 20
        if from_bottom <= 50:
            pdf_file.showPage()
            pdf_file.setFont('Arial', 14)
        from_bottom = page_height - (number % max_items_per_page) * 20
        pdf_file.drawString(
            50,
            from_bottom,
            f"{number}. {ingredient['ingredient__name']}: "
            f"{ingredient['ingredient_value']} "
            f"{ingredient['ingredient__measurement_unit']}.",
        )
    pdf_file.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def check_anonymous_return_bool(serializer, obj, model, field_name):
    """
    Проверяем существует ли запрос, анонимен ли пользователь
    и возвращаем булево значение на основе указанного поля модели
    """
    request = serializer.context['request']
    user = request.user
    if user.is_anonymous:
        return False
    return model.objects.filter(user=user, **{field_name: obj}).exists()
