import io

from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from users.models import Follow


def download_pdf(ingredients_cart):
    """Функция для отправки списка покупок в pdf"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        "attachment; filename='shopping_cart.pdf'"
    )
    pdfmetrics.registerFont(
        TTFont('Arial', 'data/arial.ttf', 'UTF-8')
    )
    buffer = io.BytesIO()
    pdf_file = canvas.Canvas(buffer)
    pdf_file.setFont('Arial', 24)
    pdf_file.drawString(200, 800, 'Список покупок.')
    pdf_file.setFont('Arial', 14)
    from_bottom = 750
    for number, ingredient in enumerate(ingredients_cart, start=1):
        pdf_file.drawString(
            50,
            from_bottom,
            f"{number}. {ingredient['ingredient__name']}: "
            f"{ingredient['ingredient_value']} "
            f"{ingredient['ingredient__measurement_unit']}.",
        )
        from_bottom -= 20
        if from_bottom <= 50:
            from_bottom = 800
            pdf_file.showPage()
            pdf_file.setFont('Arial', 14)
    pdf_file.showPage()
    pdf_file.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def check_anonymous_return_bool(self, obj, model):
    """Проверяем существует ли запрос, анонимен
    ли пользователь и возвращаем булево значение"""
    request = self.context.get('request')
    if not request or request.user.is_anonymous:
        return False
    if model == Follow:
        return model.objects.filter(
            user=request.user,
            author=obj.id
        ).exists()
    return model.objects.filter(
        recipe=obj,
        user=request.user
    ).exists()
