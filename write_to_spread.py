from openpyxl import load_workbook


def spread(output, file_path):

    wb = load_workbook(file_path)
    ws = wb.worksheets[0]

    # searches first column for an empty cell so data is appended.
    column_length = 1
    for _ in ws.rows:
        column_length += 1

    # integers in main_data and minutes_data correspond to spreadsheet column numbers.
    main_data = {'week': 1,
                 'date': 2,
                 'home_team_name': 3,
                 'away_team_name': 4,
                 'home_goal_total': 5,
                 'away_goal_total': 6,
                 'referee': 47,
                 'home_corners': 48,
                 'away_corners': 49,
                 'home_shots_on': 54,
                 'away_shots_on': 56,
                 'home_shots_wide': 55,
                 'away_shots_wide': 57,
                 'home_fouls': 52,
                 'away_fouls': 53,
                 'home_offsides': 50,
                 'away_offsides': 51,
                 'home_pens': 58,
                 'away_pens': 59,
                 'home_pen_mins': 60,
                 'away_pen_mins': 61,
                 }

    minutes_data = [('home_goal_times', 7),
                    ('away_goal_times', 15),
                    ('home_yellow_times', 23),
                    ('away_yellow_times', 32),
                    ('home_red_times', 41),
                    ('away_red_times', 44)
                    ]

    # write main_data markets.
    for key in main_data.keys():
        ws.cell(row=column_length, column=main_data[key]).value = output[key]

    # write minutes_data markets.
    for i in range(0, len(minutes_data)):
        string = minutes_data[i][0]
        length = len(output[string])
        start_col = minutes_data[i][1]
        for j in range(0, length):
            ws.cell(row=column_length, column=start_col).value = output[string][j]
            start_col += 1

    wb.save(file_path)

    print("{} - {} vs {} added.".format(output['date'], output['home_team_name'], output['away_team_name']))
