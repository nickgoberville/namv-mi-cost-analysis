import numpy as np

class Results:
    def __init__(self, results_df):
        self.index = results_df.index
        self.daily_riders_left = results_df.riders_left.to_numpy()
        self.daily_dist = results_df.daily_dist.to_numpy()
        self.daily_rides = results_df.completed_rides.to_numpy()
        self.daily_wait_times = self.get_wait_times(results_df)

    def get_wait_times(self, results_df):
        wait_times = []
        for index in self.index:
            wait_times.append(eval(results_df.wait_times_list[index]))
        return wait_times

    def get_wait_time_bins(self, min_bound, max_bound):
        count = 0
        for day in self.daily_wait_times:
            for rider_wait_time in day:
                if rider_wait_time >= min_bound and rider_wait_time < max_bound:
                    count += 1
        return count
