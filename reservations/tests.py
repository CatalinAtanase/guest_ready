import json

from django.db.models.functions import ExtractMonth
from django.db.models.functions.datetime import ExtractYear
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from reservations.constants import COMMISSIONS

from .models import Location, Reservation


class LocationTestCase(TestCase):
    def setUp(self):
        london = Location.objects.create(city="LONDON", flat="Hawtrey")
        paris = Location.objects.create(city="PARIS", flat="Malher")
        porto = Location.objects.create(city="PORTO", flat="Bragas")

    def test_location_is_showed_right(self):
        london = Location.objects.get(city="LONDON")
        paris = Location.objects.get(city="PARIS")
        porto = Location.objects.get(city="PORTO")

        self.assertEqual(str(london), 'Hawtrey in LONDON')
        self.assertEqual(str(paris), 'Malher in PARIS')
        self.assertEqual(str(porto), 'Bragas in PORTO')


class ReservationTestCase(TestCase):
    def setUp(self):
        london1 = Location.objects.create(city="LONDON", flat="Hawtrey")
        london2 = Location.objects.create(
            city="LONDON", flat="Catherine House")
        paris = Location.objects.create(city="PARIS", flat="Malher")
        porto = Location.objects.create(city="PORTO", flat="Bragas")

        r1 = Reservation.objects.create(
            reservation='HMB0001',
            checkin='2021-05-12',
            checkout='2021-06-01',
            income='1200',
            location=london1,
        )
        r2 = Reservation.objects.create(
            reservation='HMB0002',
            checkin='2021-06-02',
            checkout='2021-06-20',
            income='1150',
            location=london1,
        )
        r3 = Reservation.objects.create(
            reservation='HMB0003',
            checkin='2021-05-15',
            checkout='2021-05-20',
            income='780',
            location=london2,
        )
        r4 = Reservation.objects.create(
            reservation='HMB0004',
            checkin='2021-05-15',
            checkout='2021-06-20',
            income='1900',
            location=paris,
        )
        r5 = Reservation.objects.create(
            reservation='HMB0005',
            checkin='2021-05-30',
            checkout='2021-06-10',
            income='1350',
            location=porto,
        )
        r6 = Reservation.objects.create(
            reservation='HMB0006',
            checkin='2021-05-01',
            checkout='2021-05-12',
            income='999',
            location=porto,
        )

    def test_total_commission(self):
        response = self.client.get(
            reverse('reservations:total_commission'), follow=True
        )
        json_data = json.loads(response.content.decode('utf-8'))
        commission_from_response = json_data['commission']
        commission_from_test = 0

        reservations = Reservation.objects.all()

        for reservation in reservations:
            percentage = COMMISSIONS.get(reservation.location.city, 0)
            commission_from_test += percentage * reservation.income / 100

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(commission_from_response, commission_from_test)

    def test_commission_per_location(self):
        response = self.client.get(
            reverse('reservations:commission_for_city', args=['london']),  follow=True
        )
        json_data = json.loads(response.content.decode('utf-8'))
        commission_from_response = json_data['commission']
        commission_from_test = 0

        reservations = Reservation.objects.filter(location__city='LONDON')
        percentage = COMMISSIONS.get('LONDON', 0)

        for reservation in reservations:
            commission_from_test += percentage * reservation.income / 100

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(commission_from_response, commission_from_test)

    def test_commission_per_location_not_exist(self):
        response = self.client.get(
            reverse('reservations:commission_for_city', args=['location']), follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_commission_per_month(self):
        response = self.client.get(
            reverse('reservations:commission_per_month'),  follow=True
        )
        json_data = json.loads(response.content.decode('utf-8'))
        data_from_test = {}

        reservations = Reservation.objects.all().annotate(
            month=ExtractMonth('checkin'), year=ExtractYear('checkin'))
        for reservation in reservations:
            checkin_month = str(reservation.month).zfill(2)
            checkin_year = reservation.year
            string_date = f'{checkin_month}/{checkin_year}'
            if string_date in data_from_test:
                data_from_test[string_date] += reservation.income * \
                    COMMISSIONS[reservation.location.city] / 100
            else:
                data_from_test[string_date] = reservation.income * \
                    COMMISSIONS[reservation.location.city] / 100

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_from_test, json_data)

    def test_load_csv(self):
        with open('Reservations.xlsx', 'rb') as csv_file:
            response = self.client.post(path=reverse(
                'reservations:load_csv'), data={'guest_ready': csv_file}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
