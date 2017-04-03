<p align="center"><img align="middle" src="https://github.com/BStaff1986/NHLTravel/blob/master/OTT.gif" alt="Ottawa Senators 2016-2017"></p>

# NHLTravel

On February 9th, 2017, during the TSN broadcast of the Ottawa Senators game against the Dallas Stars, the TSN announcing team had a discussion about the travel itineraries of NHL teams. They asserted that Dallas had the worst travel schedule because their city was geographically isolated relative to other NHL cities. I thought it would be interesting to explore the data and see if their intuitions were correct. 

I grabbed a dataset containing the 2016-2017 NHL season and another dataset that contained the geocoordinates for major world cities. Whenever a team traveled to a new city, the great circle distance between the two locations was calculated. Below is a table containing the total amount each team will travel in the 2016-2017 season (excluding pre- and post-season). The average distance column describes the mean distance between the city and all other NHL cities. All distances are in kilometers.

|       City       | Total Traveled | Avg. Distance | Furthest City | Distance | Closest City     | Distance |
|------------------|----------------|---------------|---------------|----------|------------------|----------|
| Edmonton         | 79190          | 2577          | Sunrise       | 4101     | Calgary          | 281      |
| San Jose         | 78556          | 2976          | Boston        | 4310     | Los Angeles      | 492      |
| Calgary          | 77993          | 2499          | Sunrise       | 3985     | Edmonton         | 281      |
| Glendale         | 76934          | 2504          | Boston        | 3698     | Anaheim          | 530      |
| Vancouver        | 73608          | 2963          | Sunrise       | 4485     | Calgary          | 673      |
| Denver           | 72641          | 1942          | Boston        | 2840     | Glendale         | 941      |
| Dallas           | 72538          | 1884          | Vancouver     | 2842     | St. Louis        | 881      |
| Los Angeles      | 72435          | 2837          | Boston        | 4169     | Anaheim          | 38       |
| Winnipeg         | 71956          | 1842          | Sunrise       | 3017     | Saint Paul       | 628      |
| Anaheim          | 70940          | 2826          | Boston        | 4153     | Los Angeles      | 38       |
| Tampa            | 67687          | 2096          | Vancouver     | 4179     | Sunrise          | 307      |
| Sunrise          | 66841          | 2306          | Vancouver     | 4485     | Tampa            | 307      |
| Boston           | 66018          | 1820          | San Jose      | 4310     | New York City    | 305      |
| Saint Paul       | 63019          | 1545          | San Jose      | 2539     | Chicago          | 558      |
| Nashville        | 62749          | 1506          | Vancouver     | 3264     | St. Louis        | 407      |
| Montreal         | 62701          | 1744          | San Jose      | 4064     | Ottawa           | 164      |
| St. Louis        | 62266          | 1462          | Vancouver     | 2859     | Nashville        | 407      |
| Detroit          | 61417          | 1375          | San Jose      | 3333     | Columbus         | 263      |
| Raleigh          | 60898          | 1622          | Vancouver     | 3874     | Washington, D.C. | 375      |
| New York City    | 59459          | 1622          | San Jose      | 4102     | Brooklyn         | 8        |
| Chicago          | 57439          | 1390          | San Jose      | 2956     | Detroit          | 383      |
| Buffalo          | 56596          | 1444          | San Jose      | 3669     | Toronto          | 100      |
| Ottawa           | 56281          | 1640          | San Jose      | 3901     | Montreal         | 164      |
| Washington, D.C. | 54685          | 1529          | San Jose      | 3888     | Philadelphia     | 199      |
| Pittsburgh       | 53778          | 1409          | San Jose      | 3608     | Columbus         | 260      |
| Philadelphia     | 53764          | 1578          | San Jose      | 4022     | Newark           | 121      |
| Columbus         | 53454          | 1378          | San Jose      | 3363     | Pittsburgh       | 260      |
| Newark           | 52998          | 1613          | San Jose      | 4088     | New York City    | 14       |
| Toronto          | 52860          | 1453          | San Jose      | 3618     | Buffalo          | 100      |
| Brooklyn         | 52223          | 1626          | San Jose      | 4108     | New York City    | 8        |
|------------------|----------------|---------------|---------------|----------|------------------|----------|
| Average          | 64130          | 1900          |               | 3728     |                  | 316      |

As the table shows, the TSN team was wrong in their assertion that Dallas is the team that needs to travel the most. Six teams will travel more kilometers during this season than Dallas and 10 teams have greater average distances to all other NHL teams. The teams that are, on average, further from other cities than Dallas are the teams that are tucked away in the corners of North America (with the exception of the Northeastern corner). This means that Dallas's South Central location is actually helpful in limiting the distance they need to travel.

Some caveats: Distances between cities were calculates using the haversine formula. This formula measures the length of a great circle drawn between two cities and does not account for distance added from the arc of a flight path, curves on highways, or any other obstacles. The geocoordinates used mark each city's city-center and extra kilometers for travel between airports and stadiums are not represented.

After writing the code to complete the table, I decided I would use the coordinate data I had used to make a nice visualization of the data. Using matplotlib and Basemap, I was able to create an animated map for each NHL team which draws an Indiana Jones-style map of their travels throughout the 2016-2017 season.

<p align="center"><img src="https://github.com/BStaff1986/NHLTravel/blob/master/TOR.gif" alt="Toronto Maple Leafs 2016-2017" width="400"><img src="https://github.com/BStaff1986/NHLTravel/blob/master/MTL.gif" alt="Montreal Canadiens 2016-2017" width="400"></p>

Above is the Toronto Maple Leafs and Montreal Canadiens maps. To create maps for every team, or to create a map for a specific team, run basemap.py. You will need NHLTravel.py and <a href='https://ffmpeg.org/download.html'>FFMPEGWriter</a> to run the program successfully. 
