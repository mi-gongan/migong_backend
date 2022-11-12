from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from .services import Face

# Create your views here.


class Image(APIView):
    def post(self, request):
        # res = request.FILES['photo'].read()
        res = request.FILES['photo']
        print(res)
        serializers = PhotoSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            print(serializers.data['photo'])
            Face.calculate(Face, serializers.data['photo'])
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
