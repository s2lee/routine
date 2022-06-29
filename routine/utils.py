import datetime
from rest_framework.response import Response
from .models import RoutineDay

days_dict = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}
days_op_dict = {0: "MON", 1: "TUE", 2: "WED", 3: "THU", 4: "FRI", 5: "SAT", 6: "SUN"}


def get_response(data, method):
    flag = True
    if method in {"CREATE", "UPDATE", "DELETE"}:
        flag = False
    last_data = data if flag else {"routine_id": data}
    response = Response(
        {
            "data": last_data,
            "message": {"msg": "  .", "status": f"ROUTINE_{method}_OK"},
        }
    )
    return response


def convert_days_list_to_date(days):
    global days_dict

    now = datetime.datetime.now()
    data = []
    day_num = datetime.datetime.today().weekday()
    for day in days:
        diff = days_dict[day] - day_num
        converted_day = now + datetime.timedelta(days=diff)
        data.append(converted_day)
    return data


def convert_date_to_days_list(routine_obj):
    global days_op_dict

    data = []
    routine_day_qs = RoutineDay.objects.filter(routine_id=routine_obj)
    for routine_day in routine_day_qs:
        day = routine_day.day.weekday()
        data.append(days_op_dict[day])
    return data


def convert_days_list_to_date_at_update(routine_obj, days):
    global days_dict

    data = []
    routine_create_date = routine_obj.created_at
    day_num = routine_create_date.weekday()
    for day in days:
        diff = days_dict[day] - day_num
        converted_day = routine_create_date + datetime.timedelta(days=diff)
        data.append(converted_day)

    return data
