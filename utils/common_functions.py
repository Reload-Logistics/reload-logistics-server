from datetime import datetime
# ... verify job date time 
def validate_correct_date_time(booking_date : any, booking_time : any)->bool:
    # epoch
    return (datetime.\
                strptime(f"{str(booking_date)} {str(booking_time)}", '%Y-%m-%d %H:%M:%S').\
                timestamp() - datetime.now().timestamp() < 0) 