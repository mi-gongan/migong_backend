from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from .services import Face
import os
from django.conf import settings

# Create your views here.


class Analyze(APIView):
    def post(self, request):
        serializers = PhotoSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            data = Face.calculate(Face,serializers.data['photo'])
            # image remove
            os.remove(settings.BASE_DIR+serializers.data['photo'])
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
