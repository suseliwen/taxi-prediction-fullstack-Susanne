from datetime import datetime
from taxipred.utils.time_features import traffic_condition, time_of_day, day_of_week_label


def test_traffic_weekday():
    assert traffic_condition(datetime(2025,10,7,7,30))  == "High"
    assert traffic_condition(datetime(2025,10,7,12,15)) == "Medium"
    assert traffic_condition(datetime(2025,10,7,22,10)) == "Low"


def test_time_of_day():
    assert time_of_day(datetime(2025,10,7,7,30))  == "Morning"
    assert time_of_day(datetime(2025,10,7,13,0))  == "Day"
    assert time_of_day(datetime(2025,10,7,19,0))  == "Evening"
    assert time_of_day(datetime(2025,10,7,2,0))   == "Night"

def test_day_of_week_label():
    assert day_of_week_label(datetime(2025,10,7,7,30)) == "Weekday"
    assert day_of_week_label(datetime(2025,10,5,7,30)) == "Weekend"