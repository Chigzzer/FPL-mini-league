import data

print('The top gameweek scored: ' + str(data.top_gw_points))
print('The following players scored the maximum points at each of the following gameweeks')
for winner in range(len(data.top_gws)):
    print(str(data.top_gw_players[winner]) + ': ' + str(data.top_gws[winner]))


print('The top scorers for each month are below:')
for month in data.months:
    if 'top_scorer' not in month.keys():
        continue
    print(month['month_name'] + ' Top Scorers who scored: ' + str(month['top_points']) + ' are:')
    for player in month['top_scorer']:
        print(player)