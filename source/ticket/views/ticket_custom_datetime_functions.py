import datetime, businesstimedelta, pytz


def buisnesstimedelta_function(object_):
    workday = businesstimedelta.WorkDayRule(
        start_time=datetime.time(9),
        end_time=datetime.time(18),
        working_days=[0, 1, 2, 3, 4],
        tz=pytz.timezone('Asia/Bishkek'))
    businesshours = businesstimedelta.Rules([workday])
    expected_time_to_finish = object_.expected_finish_date
    time_difference = businesshours.difference(datetime.datetime.now(), expected_time_to_finish)
    return time_difference
