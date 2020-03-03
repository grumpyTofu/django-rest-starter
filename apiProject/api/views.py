from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.serializers import DataFileSerializer

import pandas as pd


class DataFileView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = DataFileSerializer(data=request.data)

        if file_serializer.is_valid():
            data_file = file_serializer.validated_data['file']

            excel = pd.read_excel(data_file)
            print(excel)
            # file_serializer.save()
            # return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            return Response('Success', status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)