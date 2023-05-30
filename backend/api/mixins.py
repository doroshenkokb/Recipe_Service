import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response


class FavoriteCart:

    def favorite_and_cart(self, request, obj_id, model, errors):
        """Функция для добавления и удаления Favorite и Cart"""
        user = request.user
        obj = model.objects.filter(user=user, recipe=obj_id)
        if request.method == 'POST':
            if obj.exists():
                return Response(
                    {'errors': errors.get('if_exists')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            obj = get_object_or_404(self.add_model, id=obj_id)
            model.objects.create(user=user, recipe=obj)
            return Response(
                self.add_serializer(obj).data, status=status.HTTP_201_CREATED

            )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': errors.get('if_deleted')},
            status=status.HTTP_400_BAD_REQUEST
        )


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для обработки изображений в формате base64"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'image.{ext}')
        return super().to_internal_value(data)
