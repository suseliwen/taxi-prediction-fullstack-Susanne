from datetime import datetime, time

def traffic_condition(dt: datetime) -> str:
    weekday = dt.weekday()
    hour = dt.hour    

    if weekday < 5:     # Måndag–fredag
        if 6 <= hour < 10 or 15 <= hour < 18:
            return "High"
        elif 10 <= hour < 15 or 18 <= hour < 21:
            return "Medium"
        else:
            return "Low"
    else:               # Lördag–söndag
        if 11 <= hour < 18:
            return "Medium"
        else:
            return "Low"
        

def time_of_day(dt: datetime) -> str:
    """Returnerar 'Morning', 'Day', 'Evening' eller 'Night' beroende på timme."""
    hour = dt.hour

    if 6 <= hour < 10:
        return "Morning"
    
    elif 10 <= hour < 17:
        return "Day"
    
    elif 17 <= hour < 22:
        return "Evening"
    
    else:
        return "Night"


def day_of_week_label(dt: datetime) -> str:
    """Returnerar 'Weekday' eller 'Weekend' beroende på datum."""
    return "Weekend" if dt.weekday() >= 5 else "Weekday"


