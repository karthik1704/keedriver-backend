const = f"""
Call Back  for further Trips %0a
%2B91 7200588582 %0a
%0a 
We are happy to serve you, Have a safe and Comfortable journey with our KeeDriver  %0a
%0a

https://g.co/kgs/M5uabU %0a
%0a
Kindly share your valuable review here with 5 Star. It will help us improving our quality of our service %0a
%0a
Thanks in Advance, %0a
Team KeeDriver %0a
www.keedriver.com %0a
%0a
Note: If you contact driver directly for further Trips , Company is not responsible any for issues 
"""


def gernerate_message(
    name, cphone, trip_type, drop_location, date, time, dname, dphone, trip_id, pick_location , is_driver, pcoordinate, dcoordinate
):
    msg=''

    drop_location_not_empty = f'*Drop location* {drop_location}'  if drop_location else '' 

    if not is_driver:
        msg = f"""
*Thank you for choosing KEEDRIVERS* %0a

Dear *{name.strip()},* %0a
Your booking details are below %0a
%0a
*Trip ID*: {trip_id} %0a
%0a
*Name* {name} %0a
%0a
*Contact* %2B91 {cphone} %0a
%0a
*Trip type* {trip_type} %0a
%0a
*Pickup location* {pick_location } %0a
%0a
{drop_location_not_empty} %0a
%0a
*Pickup Coordinates* https://maps.google.com?q={pcoordinate.coords[1]},{pcoordinate.coords[0]}
%0a
*Date:* {date} %0a
%0a
*Timing:* {time} %0a
%0a
Driver details %0a
%0a
*Driver name*  {dname} %0a
Contact %0a
%2B91 {dphone} %0a

{const} %0a
    """

    if  is_driver:
        msg = f"""
*Thank you for choosing KEEDRIVERS* %0a
%0a
Dear *{dname.strip()}*, %0a
Your customer details are below %0a
%0a
*Trip ID*: {trip_id} %0a
%0a
*Customer name* {name} %0a
%0a
*Customer contact* %2B91 {cphone} %0a
%0a
*Trip type* {trip_type} %0a
%0a
*Pickup location* {pick_location } %0a
%0a
*Pickup Coordinates* https://maps.google.com?q={pcoordinate.coords[1]},{pcoordinate.coords[0]}
%0a
{drop_location_not_empty} %0a
%0a
*Drop Coordinates* https://maps.google.com?q={dcoordinate.coords[1]},{dcoordinate.coords[0]}
%0a
*Date:* {date} %0a
%0a
*Timing:* {time} %0a
%0a
Driver details %0a
%0a
*Driver name*  {dname} %0a
Contact %0a
%2B91 {dphone} %0a

    """
    return msg
