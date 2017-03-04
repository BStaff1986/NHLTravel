import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import animation
from NHLTravel import NHLTravel
plt.rcParams['animation.convert_path'] = 'C:\\Program Files\\ImageMagick\\convert.exe'
import time

nhl = NHLTravel()

#all_teams = [nhl.convert_name_to_abbr(x) for x in nhl.sched['Home'].unique()]
# SAMPLE
all_teams = ['MIN',]

def get_colors(team):
    # First hex Code is ocean color
    # Second hex code is line color
    # Third, optional, hex code is the land color
    # Fourth, optional, hex code is border colors
    team_colors = {
                'ANA':['#F57D31', '#B6985A'],
                'ARI':['#98012E', '#024731', '#EEE3C7'],
                'ATL':'Atlanta',
                'BOS':['#FFB81C', '#000000'],
                'BUF':['#041E42', '#FFB81C', '#A2AAAD'],
                'CAL':['#C8102E', '#F1BE48'],
                'CAR':['#C8102E', '#010101', '#A2AAAD'],
                'CHI':['#C8102E', '#CC8A00'],
                'COL':['#236192', '#6F263D', '#A4A9AD'],
                'CBJ':['#041E42', '#C8102E', '#A4A9AD'],
                'DAL':['#006341', '#010101', '#8A8D8F'],
                'DET':['#C8102E', '#010101'],
                'EDM':['#00205B', '#CF4520'],
                'FLO':['#041E42', '#C8102E', '#B9975B'],
                'LA': ['#582a85', '#FFC80C'],
                'MIN':['#154734', '#EAAA00', '#DDCBA4', '#A6192E'],
                'MTL':['#C51230', '#083A81'],
                'NAS':['#041E42', '#FFB81C'],
                'NJD':['#C8102E', '#0C753B'],
                'NYI':['#003087', '#FC4C02'],
                'NYR':['#0033A0', '#C8102E'],
                'OTT':['#E51837', '#D4A00F'],
                'PHI':['#FA4616', '#010101'],
                'PHO':['#98012E', '#024731', '#EEE3C7'],
                'PIT':['#FFB81C', '#000000'],
                'SJ': ['#006272', '#E57200'],
                'STL':['#041E42', '#FFB81C'],
                'TB': ['#00205B','#010101'],
                'TOR':['#2A6EBB', '#002664'],
                'VAN':['#00205B', '#008752', '#97999B', '#041C2C'],
                'WAS':['#041E42', '#A6192E', '#A2AAAD', '#782F40'],
                'WPG':['#041E42', '#C8102E', '#ACAAAC', '#746E74'],
                   }
    if team in team_colors.keys(): 
        return team_colors[team]
    else:
        return ['#82bcff','#FF7700']

for map_team in all_teams:
    start = time.time()
    nhl = NHLTravel(map_team)

    coords = nhl.season_path()
    locs = nhl.get_lat_long() 
    
    # Colors 
    colors = get_colors(map_team)  
    
    ocean_color = colors[0]
    line_color = colors[1]
    
    if len(colors) == 3:
        land_color = colors[2]
    else:
        land_color = '#FFFFFF'
    if len(colors) == 4:
        border_color = colors[3]
    else:
        border_color = '#C0C0C0'
    
    fig = plt.figure(figsize=(8,5.32))
    # ADDED THE BELOW
    ax = plt.subplot(111)
    plt.axis('off')
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    ax.set_frame_on(False)
    
    m = Basemap(projection='merc', resolution='c',
                        llcrnrlon=-125, llcrnrlat=25, # LL = lower left
                        urcrnrlon=-60, urcrnrlat=55) #UR = upper right 
    
    m.drawlsmask(land_color = land_color, 
                   ocean_color= ocean_color,
                   resolution = 'l')
    
    m.drawcountries(color=border_color, linewidth=2)
    m.drawstates(color=border_color)
    
   
    special_cases_12x8 =     {   # First list item = Latitude
                         'Anaheim':[-0.75,-0.15],  
                         'Ottawa':[0, -2.95], 
                         'Columbus':[-0.50,0], 
                         'Los Angeles':[0.25,0.15],
                         }
    
    
    # Map (long, lat) to (x, y) for plotting
    for x in range(len(locs)):
        team = locs.iloc[x][0]
        lat, long =  locs.iloc[x][1], locs.iloc[x][2]
        
        if team in special_cases_12x8.keys():
            x, y = m(long, lat)
            plt.plot(x, y, 'ok', markersize=3)
            # Change the location of the descriptive text
            lat += special_cases_12x8[team][0]
            long += special_cases_12x8[team][1]
            x, y = m(long, lat)
            plt.text(x, y, team, fontsize=8)
        elif team  == 'Brooklyn' or team == 'Newark':
            pass
        else:
            lat += 0.1
            x, y = m(long, lat)
            plt.plot(x, y, 'ok', markersize=3)
            plt.text(x, y, team, fontsize=8)
    
    x_list = []
    y_list = []
    for index, row in coords.iterrows():
        line, = m.drawgreatcircle(row['Lon1'],row['Lat1'],
                                  row['Lon2'], row['Lat2'])
        x,y = line.get_data()
        line.remove()
        del line
        x_list.append(x)
        y_list.append(y)
        
    
    all_x = np.concatenate((x_list))
    all_y = np.concatenate((y_list))
    line, = plt.plot([],[], color=line_color, linewidth=3)
    
    
    
    def update(i):
        if i <= 20:
            line.set_data(all_x[:i], all_y[:i])
        elif i > 20: # Makes the line "fly" instead of being stuck on origin
            j = i - 6
            line.set_data(all_x[j:i], all_y[j:i])
    
           
    ani = animation.FuncAnimation(fig, update, frames=len(all_x + 40), 
                                  interval=75, repeat=False)
    writer = animation.FFMpegFileWriter(fps=24, codec=None, bitrate=1000, 
                              extra_args=None, metadata=None)
    filepath = (r'C:\Users\Bryan\Anaconda3\Python Projects\Data ' \
                + r'Visualization\NHL Schedule\Animations' + '\\' \
                + map_team + '.mp4')   
    ani.save(filepath, writer=writer, fps=30)
    
    
    
    #plt.tight_layout()
    
    end = time.time()
    print(end - start)
