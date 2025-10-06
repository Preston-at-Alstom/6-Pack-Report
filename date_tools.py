import datetime as dt

def get_date():
    #get date
    hour = int(dt.datetime.now().strftime("%H"))
    if hour >=19 and hour <24:
            date = dt.date.today() + dt.timedelta(days=1)
    else:
            date = dt.date.today()

    # from date, get month
    month = date.strftime("%B")
    if date.day >0 and date.day <10:
            day = f'0{date.day}'
    else:
        day = date.day

    # from date, get year
    year = date.year

    return month, day, year