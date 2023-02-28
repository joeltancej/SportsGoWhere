# for the API Managers to get SGT datetime 

# import pytz to get SGT
import pytz
import datetime

def get_dt():
    # set timezone to SG
    timezone = pytz.timezone('Asia/Singapore')

    # get datetime and localize it to SGT
    dt = datetime.datetime.now()
    now = timezone.localize(dt)

    # transform datetime into a format suitable for the PSI API
    param = now.strftime("%Y-%m-%d %H:%M:%S").replace(" ", "T")

    return param