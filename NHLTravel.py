'''
Extract the city locations we care about
Data from: http://www.geonames.org/ and www.leftwinglock.com
'''
####
# TODO: Collect more schedules to allow year by year 
# TODO: Allow list of teams to be selected
# TODO: Make sure on multiple year schedules that first game is always traveled
#       to from home location 
# TODO: Refactor the for loop used in three functions that gets the lat and longs
####

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from math import radians, cos, sin, asin, sqrt

class NHLTravel():
    
    def __init__(self, team='all', years=2016):
        '''
        Read in the NHL schedule and the Geolocation data sets
        '''
        self.years = years
        
        self.team = team
        
        # Read in schedules
        # TODO: Add function to make multiple years or other years be used
        self.sched = pd.read_csv('2016_2017_NHL_Schedule.csv')
        
        # Convert teams in sched to cities 
        self.sched['Home'] = self.sched['Home'].map(self.get_cities)
        self.sched['Away'] = self.sched['Away'].map(self.get_cities)
        
        # Collect all the team
        self.teams = self.sched['Home'].unique()
    
        
    def convert_cities(self, city):
        '''
        Converts state and city names to how they appear in the Geonames data
        set. Also used to locate the proper Geonames index number for cities that
        share names with other places or have been converted.
        '''
        
        convert_cities = {'Arizona': 'Glendale',
                          'Minnesota': 'Saint Paul',
                          'New Jersey': 'Newark',
                          'Florida': 'Sunrise',
                          'Carolina': 'Raleigh',
                          'Colorado': 'Denver',
                          'Washington': 'Washington, D.C.',
                          'Buffalo': 'Buffalo',
                          'Columbus': 'Columbus',
                          'Tampa Bay': 'Tampa',
                          'New York': 'New York City',
                          'New York City - Rangers': 'New York City',
                          'New York City - Islanders': 'Brooklyn',                                                    
                                     }
        
        if city in convert_cities.keys():
            return convert_cities[city]
        else:
            return city
        
    
    def convert_name_to_city(self, city_abbr):
        abbrs = {
                'ANA':'Anaheim',
                'ARI':'Glendale',
                'ATL':'Atlanta',
                'BOS':'Boston',
                'BUF':'Buffalo',
                'CAL':'Calgary',
                'CAR':'Raleigh',
                'CHI':'Chicago',
                'COL':'Denver',
                'CBJ':'Columbus',
                'DAL':'Dallas',
                'DET':'Detroit',
                'EDM':'Edmonton',
                'FLO':'Sunrise',
                'LA':'Los Angeles',
                'MIN':'Saint Paul',
                'MTL':'Montreal',
                'NAS':'Nashville',
                'NJD':'Newark',
                'NYI':'Brooklyn',
                'NYR':'New York City',
                'OTT':'Ottawa',
                'PHI':'Philadelphia',
                'PHO':'Glendale',
                'PIT':'Pittsburgh',
                'SJ':'San Jose',
                'STL':'St. Louis',
                'TB':'Tampa',
                'TOR':'Toronto',
                'VAN':'Vancouver',
                'WAS':'Washington, D.C.',
                'WPG':'Winnipeg',
        }
        city_abbr = city_abbr.upper()
        if city_abbr in abbrs.keys():  
            return abbrs[city_abbr]
        else:
            return "Not Found"
            
    def convert_name_to_abbr(self, city_name):
        abbrs = {
                 'Anaheim':'ANA',
                 'Atlanta': 'ATL',
                 'Boston': 'BOS',
                 'Brooklyn': 'NYI',
                 'Buffalo': 'BUF',
                 'Calgary': 'CAL',
                 'Chicago': 'CHI',
                 'Columbus': 'CBJ',
                 'Dallas': 'DAL',
                 'Denver': 'COL',
                 'Detroit': 'DET',
                 'Edmonton': 'EDM',
                 'Glendale': 'PHO',
                 'Los Angeles': 'LA',
                 'Montreal': 'MTL',
                 'Nashville': 'NAS',
                 'New York City': 'NYR',
                 'Newark': 'NJD',
                 'Ottawa': 'OTT',
                 'Philadelphia': 'PHI',
                 'Pittsburgh': 'PIT',
                 'Raleigh': 'CAR',
                 'Saint Paul': 'MIN',
                 'San Jose': 'SJ',
                 'St. Louis': 'STL',
                 'Sunrise': 'FLO',
                 'Tampa': 'TB',
                 'Toronto': 'TOR',
                 'Vancouver': 'VAN',
                 'Washington, D.C.': 'WAS',
                 'Winnipeg':'WPG',
                 }
        
        if city_name in abbrs.keys():  
            return abbrs[city_name]
        else:
            return "Not Found"
               
        
    def prep_sched(self):
        '''
        Take a list of the years being examined
        Return a schedule or schedules concatenated togther
        '''
        # TODO: Complete this process
        
        self.sched = pd.DataFrame()
        
        for year in self.years:
            start = year
            end = year + 1
            temp_sched = pd.read_csv('{}_{}_NHL_Schedule.csv').format(start, end)
            self.sched = pd.concat(self.sched, temp_sched)
        
        self.sched['Date'] = pd.to_datetime(self.sched['Date'])
        
        return self.sched
        
        
    def get_cities(self, team):
        '''
        To be used with Panda's Series map method. This function takes a team 
        name from a schedule and parses the city name. In the case of the New York
        Islanders, the city name is changed to Brooklyn where they play.
        '''    
        exceptions = ['Columbus', 'Toronto', 'Detroit']    
        exceptions_2 = ['Los', 'San', 'New', 'St.']
        
        team = team.split()
        
        if len(team) == 1:
            city = team[0]
            
        elif len(team) == 2:
                if team[0] in exceptions_2:
                    city = ' '.join(team[0:2])
                elif team[0] == 'NY':
                    if team[1] == 'Islanders':
                        city = 'Brooklyn'
                    elif team[1] == 'Rangers':
                        city = 'New York City'
                else:
                    city = team[0]
        elif len(team) >= 3:
            if team[0] in exceptions:
                city = team[0]
            elif team[2] == 'Islanders':
                city = 'Brooklyn'
            elif team[2] == 'Rangers':
                city = 'New York City'
            else:
                city = ' '.join(team[0:2])
        
        else:
            city = team[0]
            
        city = self.convert_cities(city)
        return city
    
    
    def get_lat_long(self):
        '''
        This function returns a DataFrame containing the NHL cities and their 
        latitudes and longitudes
        '''
        # Import the geonames data set
        na = pd.read_csv('cities15000.txt', sep='\t', 
                         header=None, error_bad_lines=False)
        
        valid_city_indices = {'Glendale' : 21695,
                          'Saint Paul' : 21183, 
                          'Newark' : 21274, 
                          'Sunrise' : 20010, 
                          'Raleigh' : 20460, 
                          'Montreal' : 2478, 
                          'Denver' : 22088,
                          'San Jose' : 21995, 
                          'Washington, D.C.' : 19820,
                          'Boston' : 20942,
                          'Buffalo' : 21334,
                          'Columbus': 20495,
                          'Tampa': 20015,
                          'New York' : 21406,
                          'New York City' : 21406,
                          'Brooklyn' : 21333,
                          'Los Angeles' : 21879,
                                     }
        
        # Get the index for each city in our schedule
        indices = []
        for city in self.teams:
            if city in valid_city_indices:
                indices.append(valid_city_indices[city])
            else:
                indices.append(na[na[2] == city].index[0])
         
        # Create a DataFrame of just the city name (#2), latitude (#4)
        # and longitude(#5)
        city_df = na.iloc[indices,[2,4,5]]
        city_df.reset_index(drop=True, inplace=True)
        city_df.columns = ['City', 'Latitude', 'Longitude']
        
        return city_df
    
    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r    
    
    def calc_travel(self): 
        # Get a dataframe with the cities and their latitudes/longitudes
        city_df = self.get_lat_long()
        
        # Choose the selected teams
        if self.team != 'all':
            # Convert abbreviations to city names
            select_team = self.convert_name_to_city(self.team)
            teams = [select_team]
        else:
            teams = city_df['City']    
        
        # Go through each team's schedule, calculating the distance 
        # traveled between games, and then adding their total to a dict
        # so each team can be compared.
        
        total_traveled = {}
        for team in teams:
            itinerary = self.sched[(self.sched['Home'] == team)| 
                                   (self.sched['Away'] == team)]
            itinerary = itinerary['Home']
            travel_dist = 0
            last_city = team #Starts on team for those who played 1st game away
            for game in itinerary:
                current_city = game
                if current_city != last_city:
                    lon1 =  city_df[city_df['City'] == last_city]['Longitude'].values[0]
                    lat1 =  city_df[city_df['City'] == last_city]['Latitude'].values[0]
                    lon2 =  city_df[city_df['City'] == current_city]['Longitude'].values[0]
                    lat2 =  city_df[city_df['City'] == current_city]['Latitude'].values[0]
                    travel_dist += self.haversine(lon1, lat1, lon2, lat2)
                else:
                                        pass
                last_city = current_city  
            total_traveled[team] = travel_dist
        return total_traveled      
        
    
    def season_path(self):
        '''
        This function prepares a list of latitudes and longitudes to be used to
        make a map with great circle flightpaths drawn on it like it were from
        an Indiana Jones movie
        '''
        city_df = self.get_lat_long()
        
        # Choose the selected teams
        if self.team != 'all':
            # Convert abbreviations to city names
            select_team = self.convert_name_to_city(self.team)
            teams = [select_team]
        else:
            print('Choose a team (ex. OTT): ')
            while True:
                select_team = input()
                select_team = self.convert_name_to_city(select_team)
                if select_team != "Not Found":
                    break
                else:
                    print('Team not found. Please try again')
            
            teams = [select_team]
        # Create a dataframe to store all the coordinates
        coords = pd.DataFrame(columns=['City1','Lon1','Lat1',
                                       'City2','Lon2','Lat2'])
        for team in teams:
            # Select all the games for our team of interest
            itinerary = self.sched[(self.sched['Home'] == team)| 
                                   (self.sched['Away'] == team)]
            
            # Only keep the home location of the team's games
            itinerary = itinerary['Home']
            
            #Starts on team for those who played 1st game away
            last_city = team 
            
            for game in itinerary:
                current_city = game
                if current_city != last_city:
                    city1 = last_city
                    lon1 =  city_df[city_df['City'] == last_city]['Longitude'].values[0]
                    lat1 =  city_df[city_df['City'] == last_city]['Latitude'].values[0]
                    city2 = current_city
                    lon2 =  city_df[city_df['City'] == current_city]['Longitude'].values[0]
                    lat2 =  city_df[city_df['City'] == current_city]['Latitude'].values[0]
                    coords.loc[len(coords)] = [city1, lon1, lat1,
                                               city2, lon2, lat2,]
                else: 
                    pass
                last_city = current_city
                
        return coords
        
    def season_travel_map(self):
        '''
        This function takes a single hockey team and draws great circle
        lines between the cities that they travel to during a season.
        '''
        # Draw the map
        season_map = self.draw_map()
        
        # Import the season's travel path
        path = self.season_path()
        #color_map = plt.get_cmap('hsv')
        for n in range(len(path)):
            season_map.drawgreatcircle(path['Lon1'].loc[n],
                                       path['Lat1'].loc[n],
                                       path['Lon2'].loc[n],
                                       path['Lat2'].loc[n], color='g')
        return season_map
        
    def draw_map(self):
        '''
        This function draws a 10x10 map of North America with the hockey
        cities labelled. Currently, Newark and Brooklyn are left out because
        they are too proximal to other some other cities.
        '''
        # Get city locations
        locs = self.get_lat_long()
        
        # Create the figure and select the locations of its map corners.
        fig = plt.figure(figsize=(10, 10))
        m = Basemap(projection='merc', resolution=None,
                    llcrnrlon=-125, llcrnrlat=25, # LL = lower left
                    urcrnrlon=-60, urcrnrlat=55) #UR = upper right 
        m.etopo(scale=0.5, alpha=0.5)
        
        # Adjust the labels so they do not overlap
        special_cases =     {   # First list item = Latitude
                             'Anaheim':[-1.15,-0.3],  
                             'Ottawa':[0, -4.75], # Great
                             'Chicago':[-0.45, -5.25], #Perfect
                             'Glendale':[-0.65, 0.25], # Fine
                             'Pittsburgh':[-1.5, -9], # Very Good
                             'Los Angeles':[0.35,-7.90],
                             'St. Louis':[-0.15,-5.80], # Perfect
                             'Washington, D.C.':[-0.85,0.50], # Very Good
                             'Detroit':[0.35,-4.05], #Good
                             'New York City':[0.35,0], #Very Good
                             'Philadelphia':[-0.65,0.1], #Perfect
                             'Columbus':[.85,-3], # Great
                             'Buffalo':[-0.8,0.1] #Perfect
                             }
        
        # Map (long, lat) to (x, y) for plotting
        for x in range(len(locs)):
            team = locs.iloc[x][0]
            lat, long =  locs.iloc[x][1], locs.iloc[x][2]
            
            if team in special_cases.keys():
                x, y = m(long, lat)
                plt.plot(x, y, 'ok', markersize=5)
                # Change the location of the descriptive text
                lat += special_cases[team][0]
                long += special_cases[team][1]
                x, y = m(long, lat)
                plt.text(x, y, team, fontsize=12)
            elif team  == 'Brooklyn' or team == 'Newark':
                pass
            else:
                lat += 0.1
                x, y = m(long, lat)
                plt.plot(x, y, 'ok', markersize=5)
                plt.text(x, y, team, fontsize=12)
                
        return m
    
    def far_and_close(self):
        '''
        This function returns a DataFrame with each cities' furthest
        and closest counterparts and the distance in kilometers between
        each.
        '''
        # Get a dataframe with the cities and their latitudes/longitudes
        city_df = self.get_lat_long()
        
        # Choose the selected teams
        if self.team != 'all':
            # Convert abbreviations to city names
            select_team = self.convert_name_to_city(self.team)
            teams = [select_team]
        else:
            teams = city_df['City']    
        
        # Create the DataFrame that will hold all our results
        result_df = pd.DataFrame(columns=['City', 'Furthest City', 'Distance (km)',
                                          'Closest City', 'Distance (km)'])
        # Iterate through all teams                        
        for team in teams:
            # Initialize all the variables used for storing the cities and 
            # their distances
            closest_dist = 5000
            clostest_city = ''
            furthest_dist = 0
            furthest_city = ''
            away_cities = self.sched['Home'].unique() # Get all the cities
            for away_city in away_cities:
                # Make sure we skip our home city
                if team != away_city:
                    lon1 =  city_df[city_df['City'] == team]['Longitude'].values[0]
                    lat1 =  city_df[city_df['City'] == team]['Latitude'].values[0]
                    lon2 =  city_df[city_df['City'] == away_city]['Longitude'].values[0]
                    lat2 =  city_df[city_df['City'] == away_city]['Latitude'].values[0]
                    travel_dist = self.haversine(lon1, lat1, lon2, lat2)
                    # Furthest city comparisons
                    if travel_dist > furthest_dist:
                        furthest_dist = travel_dist
                        furthest_city = away_city
                    # Closest city comparisons
                    if travel_dist < closest_dist:
                        closest_dist = travel_dist
                        closest_city = away_city
                        
            # Append the final results to the results DataFrame             
            result_df.loc[len(result_df)] = [team, furthest_city, furthest_dist,
                                             closest_city, closest_dist]
        # Clean the DataFrame before returning            
        result_df.sort_values(by='City', inplace = True)  
        result_df.reset_index(drop=True, inplace=True)
                 
        return result_df

