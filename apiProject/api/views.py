from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

from api.models import DataFile
from api.serializers import DataFileSerializer

import pandas as pd
import os
import sys


def convert_excel(data_file):
    excel = pd.read_excel(data_file)
    print(excel)

def convert_data(file):
    filename, file_extension = os.path.splitext(str(file))

    if file_extension == '.json':
        return 'Handle JSON'
    elif file_extension == '.xlsx':
        return 'Handle Excel'
    elif file_extension == '.txt':
        return 'Handle text'
    elif file_extension == '.csv':
        return 'Handle csv'
    else:
        raise ValueError(file_extension + " file type was not recognized. Please contact a developer.")


class DataFileView(APIView):
    parser_class = (FileUploadParser,)

    def get(self, request, format=None):
        files = [DataFileSerializer(data_file).data for data_file in DataFile.objects.all()]
        return Response(files)


    def post(self, request, *args, **kwargs):
        file_serializer = DataFileSerializer(data=request.data)
        if file_serializer.is_valid():
            data_file = file_serializer.validated_data['file']
            try:
                file_serializer.save()
                return Response(convert_data(data_file), status=status.HTTP_201_CREATED)
            except ValueError as err:
                return Response(str(err), status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataFileDetails(APIView):
    parser_class = (FileUploadParser,)

    def get_file(self, pk):
        try:
            return DataFile.objects.get(pk=pk)
        except DataFile.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        data_file = self.get_file(pk)
        serializer = DataFileSerializer(data_file)
        return Response(serializer.data)


    def delete(self, request, pk, format=None):
        data_file = self.get_file(pk)
        data_file.delete()
        return Response(DataFileSerializer(data_file).data, status=status.HTTP_204_NO_CONTENT)


    def put(self, request, pk, format=None):
        data_file = self.get_file(pk)
        serializer = DataFileSerializer(data_file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
