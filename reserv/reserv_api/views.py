from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reserve, Table
from datetime import time, datetime


class AddReserve(APIView):
    """Добавить резерв"""
#    queryset = Reserve.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def post(self, request, format=None):
        print(request.data)
        try:
            phone = str(request.data['phone'])
            rtime = str(request.data['time'])
            duration = str(request.data['duration'])
            places = int(request.data['persons'])
            hour, minute = rtime.split(':',1)
            rtime = time(int(hour),int(minute))
            etime = time(int(hour)+int(duration),int(minute))
            today = datetime.now().date()
        except ValueError:
            return Response({"free":"0"})
        start_time = datetime.combine(today,rtime)
        end_time = datetime.combine(today,etime)
        tables = Table.objects.filter(places__gte=places)
        if tables.count() == 0:
            return Response({"free":"0"})
        reserves = Reserve.objects.filter(table__in=tables)
        reserves = reserves.filter(start_time__lt=start_time, end_time__gt=start_time)
        reserves = reserves.filter(start_time__lt=end_time, end_time__gt=end_time)
        reserves = reserves.filter(start_time__gt=start_time, end_time__lt=end_time)
        if reserves.count() == 0:
            reserve = Reserve()
            reserve.phone=phone
            reserve.start_time=start_time
            reserve.end_time=end_time
            reserve.table=tables[0]
            reserve.save()
            return Response({"free":"1"})
        return Response({"free":"0"})

    @classmethod
    def get_extra_actions(cls):
        return []


class CheckTable(APIView):
    """Проверить наличие столиков"""
#    queryset = Reserve.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def post(self, request, format=None):
        print(request.data)
        try:
            places = int(request.data['persons'])
        except ValueError:
            return Response({"got_table":"0"})
        tables = Table.objects.filter(places__gte=places)
        if (count:=tables.count()) > 0:
            return Response({"got_table":str(count)})
        else:
            return Response({"got_table":"0"})

    def get(self, request, format=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @classmethod
    def get_extra_actions(cls):
        return []
