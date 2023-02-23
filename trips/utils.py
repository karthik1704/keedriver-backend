const = """
Call Back  for further Trips
+91-7200588582

We are happy to serve you, Have a safe and Comfortable journey with our KeeDriver 

Kee Driver ( Call Driver , Acting driver, Driving Class )
Chrompet, Chennai.
https://g.co/kgs/M5uabU

Kindly share your valuable Review here 👆🏻 with 5 Star.. It is used to improve our services quality and more efficiency.

Thanks in Advance
By
KeeDriver
www.keedriver.com

Note: If you Book Driver for further Trips   directly to driver, Company not responsibility any issues
"""


def gernerate_message(
    name, cphone, trip_type, drop_location, date, time, dname, dphone
):

    msg = f"""
WELCOME TO KEEDRIVERS

CUSTOMER DETAILS

*Name* {name}

*Contact* {cphone}

{trip_type} {drop_location}

*Date:* {date}

*Timing:* {time}

Driver Details

*Driver Name*  {dname}

Contact
+91{dphone}

{const}
    """
    return msg
