import data

print("The top gameweek scored: {} points".format(data.top_gw_points))
print("The following players scored the maximum points at each of the following gameweeks: {} at {}".format(*data.top_gw_players, *data.top_gws))
"""for winner in range(len(data.top_gws)):
    print(str(data.top_gw_players[winner]) + ': ' + str(data.top_gws[winner]))"""


print('The top scorers for each month are below:')
for month in data.months:
    if 'top_scorer' not in month.keys():
        continue
    print("{} Managers of the Month are: {}, who scored {} points".format(month['month_name'], *month['top_scorer'], month['top_points'] ))

