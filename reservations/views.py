import openpyxl
from django.db.models import F, Sum
from django.db.models.expressions import Case, When
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from reservations.constants import COMMISSIONS
from reservations.models import Location, Reservation

from .constants import COMMISSIONS_BY_CITY


@api_view(('GET',))
def total_commission(request):
    reservations = Reservation.objects.all()
    commission = 0

    for reservation in reservations:
        percentage = COMMISSIONS.get(reservation.location.city, 0)
        commission += percentage * reservation.income / 100

    data = {
        'commission': commission,
    }

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(('GET',))
def commission_per_month(request):
    metrics = COMMISSIONS_BY_CITY
    result = Reservation.objects.values(
        'checkin__month', 'checkin__year'
    ).annotate(**metrics).order_by('checkin__year', 'checkin__month')

    data = {}

    for r in result:
        checkin_month = str(r.get('checkin__month', '')).zfill(2)
        checkin_year = r.get('checkin__year', '')
        string_date = f'{checkin_month}/{checkin_year}'
        data[string_date] = r.get('commission', 0)

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(('GET',))
def commission_by_city(request):
    metrics = COMMISSIONS_BY_CITY
    result = Reservation.objects.values(
        'location__city'
    ).annotate(**metrics).order_by('location__city')

    data = {}
    response_status = status.HTTP_404_NOT_FOUND

    for r in result:
        city = r.get('location__city', '')
        data[city] = r.get('commission', 0)
        response_status = status.HTTP_200_OK

    response = Response(data=data, status=response_status)

    return response


@api_view(('GET',))
def commission_for_city(request, city: str):
    # transform city to uppercase so we can query the db and get the value from COMMISSIONS
    city = city.upper()
    percentage = COMMISSIONS.get(city, 0)
    metrics = {
        'commission':  Sum(F('income') * percentage / 100)
    }
    data = Reservation.objects.filter(
        location__city=city
    ).aggregate(**metrics)

    response_status = status.HTTP_200_OK if percentage > 0 else status.HTTP_404_NOT_FOUND
    response = Response(data=data, status=response_status)

    return response


def load_csv(request):
    if "POST" == request.method:
        excel_file = request.FILES.get("guest_ready", None)
        try:
            wb = openpyxl.load_workbook(excel_file)

            worksheet = wb["Sheet1"]

            excel_data = list()
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)

            for index, row in enumerate(excel_data):
                if index == 0:
                    continue
                location, created = Location.objects.get_or_create(
                    flat=row[3], city=row[4])
                Reservation.objects.get_or_create(
                    reservation=row[0],
                    checkin=row[1].split(' ')[0],
                    checkout=row[2].split(' ')[0],
                    income=float(row[5]),
                    location=location,
                )

            return render(request, 'reservations/load_csv.html', {"excel_data": excel_data})
        except:
            return render(request, 'reservations/load_csv.html')
    else:
        return render(request, 'reservations/load_csv.html')
