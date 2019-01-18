from openpyxl import load_workbook


def spread(file_path, output):
    global i
    wb = load_workbook(file_path)
    ws = wb.worksheets[0]

    column_length = 1

    for i in ws.rows:
        column_length += 1

    column_dict = {'date': 1,
                   'home_team_name': 2,
                   'away_team_name': 3,
                   'home_goal_total': 4,
                   'away_goal_total': 5,
                   'referee': 44,
                   'home_corners': 45,
                   'away_corners': 46,
                   'home_shots_on': 51,
                   'away_shots_on': 53,
                   'home_shots_wide': 52,
                   'away_shots_wide': 54,
                   'home_fouls': 49,
                   'away_fouls': 50,
                   'home_offsides': 47,
                   'away_offsides': 48,
                   }

    for key in column_dict.keys():
        ws.cell(row=column_length, column=column_dict[key]).value = output[key]

    h1 = 6
    j = 0

    for i in output['home_goal_times']:
        ws.cell(row=column_length, column=h1).value = output['home_goal_times'][j]
        h1 += 1
        j += 1

    a1 = 14
    j = 0

    for i in output['away_goal_times']:
        ws.cell(row=column_length, column=a1).value = output['away_goal_times'][j]
        a1 += 1
        j += 1

    hy1 = 20
    j = 0

    for i in output['home_yellow_times']:
        ws.cell(row=column_length, column=hy1).value = output['home_yellow_times'][j]
        hy1 += 1
        j += 1

    ay1 = 29
    j = 0

    for i in output['away_yellow_times']:
        ws.cell(row=column_length, column=ay1).value = output['away_yellow_times'][j]
        ay1 += 1
        j += 1

    hr1 = 38
    j = 0

    for i in output['home_red_times']:
        ws.cell(row=column_length, column=hr1).value = output['home_red_times'][j]
        hr1 += 1
        j += 1

    ar1 = 41
    j = 0

    for i in output['away_red_times']:
        ws.cell(row=column_length, column=ar1).value = output['away_red_times'][j]
        ar1 += 1
        j += 1

    wb.save(file_path)

    print("{} - {} vs {} added.".format(output['date'], output['home_team_name'], output['away_team_name']))
