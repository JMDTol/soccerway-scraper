from openpyxl import load_workbook


def spread(output, file_path):
    global i

    wb = load_workbook(file_path)
    ws = wb.worksheets[0]

    column_length = 1

    for i in ws.rows:
        column_length += 1

    # dict values correspond to columns in spreadsheet
    column_dict = {'date': 1,
                   'home_team_name': 2,
                   'away_team_name': 3,
                   'home_goal_total': 4,
                   'away_goal_total': 5,
                   'referee': 46,
                   'home_corners': 47,
                   'away_corners': 48,
                   'home_shots_on': 53,
                   'away_shots_on': 55,
                   'home_shots_wide': 54,
                   'away_shots_wide': 56,
                   'home_fouls': 51,
                   'away_fouls': 52,
                   'home_offsides': 49,
                   'away_offsides': 50,
                   }

    # write minute related markets
    for key in column_dict.keys():
        ws.cell(row=column_length, column=column_dict[key]).value = output[key]

    home_goal_col = 6
    j = 0

    for i in output['home_goal_times']:
        ws.cell(row=column_length, column=home_goal_col).value = output['home_goal_times'][j]
        home_goal_col += 1
        j += 1

    away_goal_col = 14
    j = 0

    for i in output['away_goal_times']:
        ws.cell(row=column_length, column=away_goal_col).value = output['away_goal_times'][j]
        away_goal_col += 1
        j += 1

    home_yel_col = 22
    j = 0

    for i in output['home_yellow_times']:
        ws.cell(row=column_length, column=home_yel_col).value = output['home_yellow_times'][j]
        home_yel_col += 1
        j += 1

    away_yel_col = 31
    j = 0

    for i in output['away_yellow_times']:
        ws.cell(row=column_length, column=away_yel_col).value = output['away_yellow_times'][j]
        away_yel_col += 1
        j += 1

    home_red_col = 40
    j = 0

    for i in output['home_red_times']:
        ws.cell(row=column_length, column=home_red_col).value = output['home_red_times'][j]
        home_red_col += 1
        j += 1

    away_red_col = 43
    j = 0

    for i in output['away_red_times']:
        ws.cell(row=column_length, column=away_red_col).value = output['away_red_times'][j]
        away_red_col += 1
        j += 1

    wb.save(file_path)

    print("{} - {} vs {} added.".format(output['date'], output['home_team_name'], output['away_team_name']))
