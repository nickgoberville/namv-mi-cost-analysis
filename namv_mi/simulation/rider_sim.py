import os, sys
sys.path.append(os.getcwd()+'/..')
from random import randint, gauss
from cost_model.cost_model import *
import pandas as pd
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Identify verbose output.', action='store_true', default=False)    
parser.add_argument('run_number', help='Identify which simulation scenario to run.', type=int)
args = parser.parse_args()
run_num = args.run_number
verbose = args.verbose

sim_params = read_json('scenario_' + str(run_num) + '/ride_sim_params.json')

def travel_t(dist, vel, accel):
    accel_t = vel/accel * 2 # time for accel and decel (s)
    accel_s = vel*(accel_t/3600)/2 # accel/decel total distance
    remaining_dist = dist-accel_s
    constant_t = remaining_dist/vel*3600
    
    #print(dist, vel, accel, accel_t, accel_s, remaining_dist, constant_t)
    return accel_t+constant_t

class Rider:
    def __init__(self):
        #TODO: add attribute for rider waiting time
        self.pos = randint(0, sim_params['stops']-1)
        self.waiting = True
        self.start_t = 0
        self.end_t = 0

        self.stop = randint(0, sim_params['stops']-1)

        while self.pos == self.stop:
            self.stop = randint(0, sim_params['stops']-1)

class Shuttle:
    def __init__(self, vehicle):
        self.riders = []        
        self.max_riders = vehicle.passengers
        self.pos = 0    # start at stop 1

    def next_stop(self):
        self.pos += 1
        if self.pos > sim_params['stops']-1:
            self.pos = 0

    def dropoff_riders(self, verbose=True):
        index = 0
        dropped = 0
        for rider in self.riders:
            if rider.stop == self.pos:
                del self.riders[index]
                dropped += 1
            index+=1
        if verbose: print("\tDropped off {} riders.".format(dropped))
        return dropped

    def pickup_riders(self, rider_list, sim_time, verbose=True):
        index = 0
        picked = 0
        stop_riders = len(rider_list)
        vehicle_riders = len(self.riders)
        wait_t = []

        while (len(self.riders) < self.max_riders) and (len(rider_list) > 0):
            self.riders.append(rider_list[0])
            wait_t.append(sim_time - rider_list[0].start_t)
            del rider_list[0]
            picked+=1
            index+=1
        
        if verbose:
            print("\tPicked up {} riders.".format(picked))
            if stop_riders !=  picked:            
                print("\t\tHAD TO LEAVE {} RIDERS".format(stop_riders-picked))
        return rider_list, wait_t   # return remaining riders

class Stop:
    def __init__(self, id):
        self.id = id
        self.rider_list = []

        avg_dist = sim_params['loop distance']/sim_params['stops']
        self.next_dist = gauss(avg_dist, 0.1*avg_dist)

class Simulator:
    def __init__(self, start_riders, vehicle):
        # initialize Shuttle
        self.shuttle = Shuttle(vehicle)

        self.time = 0   #seconds
       
        # initialize stops
        self.stops = []
        for i in range(sim_params['stops']):
            self.stops.append(Stop(i))

        # initialize riders
        for i in range(start_riders):
            self.add_rider()

    def add_rider(self):
        rider = Rider()
        rider.start_t = self.time
        stop_id = rider.pos
        self.stops[stop_id].rider_list.append(rider)


    def reset(self, start_riders):
        # Reset stops
        for i in range(sim_params['stops']):
            self.stops[i].rider_list = []

        # Reinitalize riders at stops
        for i in range(start_riders):
            rider = Rider()
            stop_id = rider.pos
            self.stops[stop_id].rider_list.append(rider)

        # Remove riders from shuttle and put shuttle at starting
        self.shuttle.pos = 0
        self.shuttle.riders = []

        self.time = 0

#def travel_time(dist):
#    vel = sim_params['avg speed']   # in mph
#    del_t = dist / vel * 3600       # convert from hour to sec
#    return del_t

def main(vehicle, real_time=False, verbose=False, time_factor=10):
    # initialize sim
    sim = Simulator(sim_params['initial riders'], vehicle)

    # init lists for weeks
    weeks = []

    # for weeks defined in simulator param file
    for wk in range(sim_params['weeks/year']):
        days = []
        # for days defined in simulator param file
        for dy in range(sim_params['days/week']):
            data = {"riders_left_behind": 0} # store data for miles travelled, completed rides, average distance per ride, missed rides, 
            
            # For hours define in simulator param file
            sim.reset(sim_params['initial riders'])

            # Distance travelled counter
            total_dist = 0

            # Completed rides counter
            completed_rides = 0

            # Times shuttle was too small (had to leave a rider behind)
            too_small = 0

            # Frequency a new rider enters the route (seconds)
            new_rider_time = sim_params['new rider freq']

            # Place holder for last time a new rider was added to the sim
            prev_new_rider_time = 0

            # Ho many seconds for dropoff/pickup
            time_at_stop = 5

            # iterator counter
            iter = 0

            # Set wait_times list for later analysis
            wait_times = []

            # Max accel/decel
            # TODO: Add this parameter to the json file
            a = 13.5 # mph/s

            while sim.time < sim_params['hours/day']*3600:   # while time is less than day hours of operation

                if verbose: print("========\nInteration {}.\n".format(iter))
                if verbose: print("\tStops status:")
                for stop in sim.stops:
                    if verbose: print("\tStop: {} has {} riders".format(stop.id, len(stop.rider_list)))
                
                if verbose: 
                    print("\n\tShuttle status")
                    print("\tShuttle pos: {}".format(sim.shuttle.pos))
                    print("\tShuttle riders: {}".format(len(sim.shuttle.riders)))

                # current shuttle position (which stop it is at)
                shuttle_pos = sim.shuttle.pos

                # Distance to next stop
                next_dist = sim.stops[shuttle_pos].next_dist
                
                # How many riders waiting at current stop
                stop_riders = sim.stops[shuttle_pos].rider_list

                # calculating time to get to next stop
                travel_time = travel_t(next_dist, sim_params['avg speed'], a)

                # Drop off riders if this is their stop
                if verbose: print("\nDropping off riders")
                if real_time: time.sleep(time_at_stop/time_factor)
                dropped = sim.shuttle.dropoff_riders(verbose=verbose)
                completed_rides += dropped

                # Pick up new riders at the stop
                if verbose: print("\nPicking up riders.")
                if real_time: time.sleep(time_at_stop/time_factor)
                left_behind, wait_t = sim.shuttle.pickup_riders(stop_riders, sim.time, verbose=verbose)
                if len(left_behind) > 0:
                    too_small += 1

                # Get wait time stats
                for t in wait_t:
                    wait_times.append(t)

                # Move to next shuttle stop
                if verbose: print("\nTraveling to next stop.")
                if real_time: time.sleep(travel_t/time_factor)
                sim.shuttle.next_stop()

                # Update simulator time
                sim.time += travel_time + time_at_stop*(dropped + (len(stop_riders)-len(left_behind)))
                
                # Add distance travelled
                total_dist += next_dist

                if verbose: print("{} seconds passed.".format(sim.time))

                # Add new rider at frequency set before while loop
                if (sim.time - prev_new_rider_time) // new_rider_time > 0:
                    if verbose: print("Adding new rider!")
                    sim.add_rider()
                    prev_new_rider_time = sim.time

                # increase iter
                iter+=1
                if verbose: time.sleep(0.2)
            if verbose: print("Finished week {} day {}".format(wk, dy))
            # Update data dict
            data["riders_left_behind"] = too_small
            data["wait times"] = wait_times
            data["distance"] = total_dist
            data["completed_rides"] = completed_rides
            days.append(data)

            if verbose: ("\n\n{} completed rides.".format(completed_rides))
            if verbose: print("{} miles traveled.".format(total_dist))
            if verbose: print("Had to leave riders behind {} times.".format(too_small))

        weeks.append(days)

    print("========== FINISHED {} Simulation ==========".format(vehicle.name))
    print("Num weeks: {} num days: {} num data: {}".format(len(weeks), len(weeks[0]), len(weeks[0][0])))
    print("Sim time: {} Input time: {}".format(sim.time, sim_params['hours/day']*3600))
    return weeks

def data_to_year_csv(week_list, output_filename):
    df_dict = {'riders_left': [],
                'daily_dist': [],
                'completed_rides': [],
                'wait_times_list': []}

    for day in week_list:
        for data in day:
            df_dict['riders_left'].append(data["riders_left_behind"])
            df_dict['daily_dist'].append(data["distance"])
            df_dict['completed_rides'].append(data["completed_rides"])
            df_dict['wait_times_list'].append(data["wait times"])

    df = pd.DataFrame(df_dict, columns=df_dict.keys())
    df.to_csv(output_filename, index=True, header=True)

if __name__ == '__main__':
    vehicles = pd.read_csv('vehicles.csv')
    modes = read_json('modes.json')
    models_dict = {}

    for index in vehicles.index:
        vehicle = model(vehicles, index, miles_per_year=0, inflation=False, mode='normal')
        week_list = main(vehicle, real_time=False, verbose=False)
        output_filename = "sim_results/" + vehicle.name + ".csv"
        data_to_year_csv(week_list, output_filename)
    