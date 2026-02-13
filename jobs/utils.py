import datetime

def time_choices(start_hour=8, end_hour=20, interval_minutes=30):
    choices = []
    current = datetime.datetime.combine(
        datetime.date.today(),
        datetime.time(start_hour, 0)
    )
    end = datetime.datetime.combine(
        datetime.date.today(),
        datetime.time(end_hour, 0)
    )

    while current <= end:
        t = current.time()
        choices.append(
            (t.strftime("%H:%M"), t.strftime("%I:%M %p"))
        )
        current += datetime.timedelta(minutes=interval_minutes)

    return choices
