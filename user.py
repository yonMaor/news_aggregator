import datetime
import datetime as dt

class User:
    # TODO add a function that checks categories entered
    def __init__(self, source, loop_interval, **kwargs):
        self.loop_interval = loop_interval
        if source == 'database':
            user = kwargs['user']
            self.id = user[0]
            self.name = user[1]
            self.email = user[2]
            self.category = user[3]
            self.timing = user[4]
            self.timing_day = user[5]
            self.timing_hour = user[6]
            self.last_update = user[7]
            self.next_update = user[8]

        elif source == 'new_user':
            self.name = kwargs['name']
            self.email = kwargs['email']
            self.category = kwargs['category']
            self.timing = kwargs['timing']
            self.timing_day = kwargs['timing_day']
            self.timing_hour = kwargs['timing_hour']
            self.last_update = kwargs['last_update']
            time_now = dt.datetime.now()
            delta = dt.timedelta(0, self.loop_interval)
            time_now_with_delta = time_now + delta
            time_now_with_delta = int(time_now_with_delta.strftime('%y%m%d%H%M'))
            self.next_update = self.get_next_update_time(time_now_with_delta)

    def get_next_update_time(self, time_now_with_delta):
        #Returns the next update time according to the timing type chosen by the user
        if self.loop_interval > 60:
            self.loop_interval = self.loop_interval % 60
        if self.timing == 'ASAP':
            next_update_time = time_now_with_delta + self.loop_interval
        elif self.timing == 'Daily':
            next_update_time = time_now_with_delta + datetime.timedelta(days=1)
            next_update_time = next_update_time.replace(hour=self.timing_hour, minute=0)
        elif self.timing == 'Weekly':
            day_today = datetime.datetime.now().weekday()
            next_update_time = time_now_with_delta + datetime.timedelta(days=7 - day_today)
            next_update_time = next_update_time.replace(hour=self.timing_hour, minute=0)
        return next_update_time

    def set_next_update_time(self, time_now_with_delta, database):

        next_update_time = self.get_next_update_time(time_now_with_delta)

        query_text = 'UPDATE user SET next_update=? WHERE email=?'
        query_data = (int(next_update_time), self.email,)
        database.update_database(query_text=query_text, query_data=query_data)

