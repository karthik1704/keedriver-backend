const = """
Call Back  for further Trips %0a
+91-7200588582 %0a
 
We are happy to serve you, Have a safe and Comfortable journey with our KeeDriver  %0a


https://g.co/kgs/M5uabU %0a

Kindly share your valuable review here with 5 Star. It will help us improving our quality of our service %0a

Thanks in Advance, %0a
Team KeeDriver %0a
www.keedriver.com %0a

Note: If you contact driver directly for further Trips , Company is not responsible any for issues 
"""


def gernerate_message(
    name, cphone, trip_type, drop_location, date, time, dname, dphone, trip_id, pick_location , is_driver
):
    msg=''

    drop_location_not_empty = f'*Drop location* {drop_location}'  if drop_location else '' 

    if not is_driver:
        msg = f"""
Thank you for choosing KEEDRIVERS %0a

Dear *{name}*, %0a

Your booking details are below %0a

*Trip ID*: {trip_id} %0a

*Name* {name} %0a

*Contact* {cphone} %0a

*Trip type* {trip_type} %0a

*Pickup location* {pick_location } %0a

{drop_location_not_empty} %0a

*Date:* {date} %0a

*Timing:* {time} %0a

Driver details %0a

*Driver name*  {dname} %0a

Contact %0a
+91{dphone} %0a

{const} %0a
    """

    if not is_driver:
        msg = f"""
Thank you for choosing KEEDRIVERS %0a

Dear *{dname}*, %0a

Your customer details are below %0a

*Trip ID*: {trip_id} %0a

*Customer name* {name} %0a

*Customer contact* {cphone} %0a

*Trip type* {trip_type} %0a

*Pickup location* {pick_location } %0a

{drop_location_not_empty} %0a

*Date:* {date} %0a

*Timing:* {time} %0a

Driver details %0a

*Driver name*  {dname} %0a

Contact %0a
+91{dphone} %0a

    """
    return msg
