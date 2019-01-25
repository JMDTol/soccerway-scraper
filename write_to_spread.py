from openpyxl import load_workbook


def spread(output, file_path):
    global i

    wb = load_workbook(file_path)
    ws = wb.worksheets[0]

    column_length = 1

    for i in ws.rows:
        column_length += 1

    # dictionary values correspond to columns in spreadsheet where data should be written to
    main_data = {'date': 1,
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
                 'home_pens': 57,
                 'away_pens': 58,
                 'home_pen_mins': 59,
                 'away_pen_mins': 60
                 }

    minutes_data = [('home_goal_times', 6),
                    ('away_goal_times', 14),
                    ('home_yellow_times', 22),
                    ('away_yellow_times', 31),
                    ('home_red_times', 40),
                    ('away_red_times', 43)
                    ]

    # write main_data markets to spreadsheet
    for key in main_data.keys():
        ws.cell(row=column_length, column=main_data[key]).value = output[key]

    # write minutes_data markets to spreadsheet
    for i in range(0, len(minutes_data)):
        string = minutes_data[i][0]
        length = len(output[string])
        start_col = minutes_data[i][1]
        for j in range(0, length):
            ws.cell(row=column_length, column=start_col).value = output[string][j]
            start_col += 1

    wb.save(file_path)

    print("{} - {} vs {} added.".format(output['date'], output['home_team_name'], output['away_team_name']))
