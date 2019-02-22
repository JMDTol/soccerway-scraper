from openpyxl import load_workbook


def spread(output, file_path):

    wb = load_workbook(file_path)
    ws = wb.worksheets[0]

    # search first column for an empty cell so data is appended.
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

    minutes_data = {'home_goal_times': 7,
                    'away_goal_times': 15,
                    'home_yellow_times': 23,
                    'away_yellow_times': 32,
                    'home_red_times': 41,
                    'away_red_times': 44
                    }
    # Write main_data markets to sheet.
    for key in main_data.keys():
        ws.cell(row=column_length, column=main_data[key]).value = output[key]

    # Write minutes_data markets to sheet.
    for i in range(0, len(minutes_data)):
            for key in minutes_data:
                number_elements = len(output[key])
                start_col = minutes_data[key]
                for j in range(0, number_elements):
                    ws.cell(row=column_length, column=start_col).value = output[key][j]
                    start_col += 1

    wb.save(file_path)

    print("{} - {} vs {} added.".format(output['date'], output['home_team_name'], output['away_team_name']))
