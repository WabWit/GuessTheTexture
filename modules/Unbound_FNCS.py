import time

def Get_Time_Difference(start_time: int) -> int:
    current_time = int(time.time())
    difference = current_time - start_time
    return difference