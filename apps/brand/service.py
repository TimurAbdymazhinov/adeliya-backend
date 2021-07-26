from datetime import datetime

from rest_framework import exceptions

from haversine import haversine

from apps.brand.models import WorkTime
from core.constants import WEEKDAY


class FilialService:
    """
        Service for check filial status
    """

    @staticmethod
    def check_filial_status(filial_obj) -> bool:
        time_now = datetime.now().time()
        weekday_now = datetime.today().weekday() + 1
        work_time = WorkTime.objects.filter(filial=filial_obj, day=weekday_now).first()
        try:
            check_is_filial_open = (
                    work_time.start_work <= time_now <= work_time.end_work
            )
        except TypeError:
            return False
        except AttributeError:
            return False

        return check_is_filial_open

    @staticmethod
    def get_geolocation(request):
        geo_lat = request.GET.get('lat')
        geo_long = request.GET.get('long')

        if geo_lat and geo_long:
            try:
                geo_lat = float(geo_lat)
                geo_long = float(geo_long)
            except Exception:
                raise exceptions.ValidationError(
                    {'geolocation': 'Неправильный формат query param: lat long'}
                )
            return geo_lat, geo_long

        return None

    @staticmethod
    def calculate_distance(filial_geolocation, client_geolocation):
        if not client_geolocation:
            return None

        filial_geolocation = tuple(map(float, filial_geolocation.split(',')))

        return haversine(filial_geolocation, client_geolocation)


class WorkDayService:

    @staticmethod
    def create_weekday(filial_obj):
        work_days = []
        for day in range(7):
            works_time_obj = WorkTime(day=day + 1, filial=filial_obj)
            work_days.append(works_time_obj)
        WorkTime.objects.bulk_create(work_days)

    @classmethod
    def get_weekday(cls, filial_obj):
        """ Get workdays data in WorkTime model"""
        workdays = WorkTime.objects.filter(filial=filial_obj)
        data = cls.get_work_time(workdays)
        return data

    @classmethod
    def get_work_time(cls, workdays):
        """ Getting works time for JSON response """
        output_data = workdays
        raw_data = cls.get_raw_data(output_data)
        data = cls.sort_raw_data(raw_data)

        return data

    @staticmethod
    def get_raw_data(output_data):
        """ Getting raw data """
        raw_data = []

        for item in output_data:
            if item.start_work is None or item.end_work is None:
                data = {
                    'days': WEEKDAY[item.day],
                    'time': 'ВЫХ',
                    'isWeekends': True
                        }
                raw_data.append(data)
            else:
                data = {
                    'days': WEEKDAY[item.day],
                    'time': f'{str(item.start_work)[:5]} - {str(item.end_work)[:5]}',
                    'isWeekends': False
                }
                raw_data.append(data)

        return raw_data

    @staticmethod
    def sort_raw_data(raw_data):
        """ Sorted raw data for JSON response """
        raw_data_copy = raw_data.copy()
        for i in raw_data:
            for j in raw_data_copy:
                if i['time'] == j['time']:
                    if i['days'] == j['days']:
                        continue
                    else:
                        i['days'] += f"    {j['days']}"
                        raw_data.remove(j)
        return raw_data
