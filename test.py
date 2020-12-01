import unittest
from datetime import datetime, timedelta 

from main_work import is_time_for_snapshot, is_time_for_snapshot_5min

format = "%Y-%d-%m-%H-%a %H:%M:%S"

class TestSum(unittest.TestCase):
    # def test_every_monday(self): #every Monday 09:00 am
    #     start_datetime = datetime(2020, 1, 1)
    #     end_datetime = datetime(2020, 1, 30)
    #     while start_datetime <= end_datetime:
    #         if is_time_for_snapshot(start_datetime):
    #             print(start_datetime.strftime(format)) 
    #         # self.assertFalse(is_time_for_snapshot(start_datetime))
    #         start_datetime += timedelta(seconds = 1)
    def test_every_5mins(self):
        start_datetime = datetime(2020, 1, 1)
        end_datetime = datetime(2020, 1, 2)
        while start_datetime <= end_datetime:
            if is_time_for_snapshot_5min(start_datetime):
                print(start_datetime.strftime(format)) 
            # self.assertFalse(is_time_for_snapshot(start_datetime))
            start_datetime += timedelta(seconds = 1)

if __name__ == '__main__':
    unittest.main()