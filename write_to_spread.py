from openpyxl import load_workbook

def spread(file_path, output):
    wb = load_workbook(file_path)
    ws = wb.worksheets[0]

    column_length = 1

    for row in ws.rows:
        column_length += 1

    ws.cell(row=column_length, column=1).value = output['date']
    ws.cell(row=column_length, column=2).value = output['home_team_name']
    ws.cell(row=column_length, column=3).value = output['away_team_name']
    ws.cell(row=column_length, column=4).value = output['home_goal_total']
    ws.cell(row=column_length, column=5).value = output['away_goal_total']
    ws.cell(row=column_length, column=44).value = output['referee']
    ws.cell(row=column_length, column=45).value = output['home_corners']
    ws.cell(row=column_length, column=46).value = output['away_corners']
    ws.cell(row=column_length, column=47).value = output['home_offsides']
    ws.cell(row=column_length, column=48).value = output['away_offsides']
    ws.cell(row=column_length, column=49).value = output['home_fouls']
    ws.cell(row=column_length, column=50).value = output['away_fouls']
    ws.cell(row=column_length, column=51).value = output['home_shots_on']
    ws.cell(row=column_length, column=52).value = output['home_shots_wide']
    ws.cell(row=column_length, column=53).value = output['away_shots_on']
    ws.cell(row=column_length, column=54).value = output['away_shots_wide']


    H1 = 6
    j = 0

    for i in output['home_goal_times']:
        ws.cell(row=(column_length), column=H1).value = output['home_goal_times'][j]
        H1 += 1
        j += 1

    A1 = 14
    j = 0

    for i in output['away_goal_times']:
        ws.cell(row=(column_length), column=A1).value = output['away_goal_times'][j]
        A1 += 1
        j += 1

    HY1 = 20
    j = 0

    for i in output['home_yellow_times']:
        ws.cell(row=(column_length), column=HY1).value = output['home_yellow_times'][j]
        HY1 += 1
        j += 1

    AY1 = 29
    j = 0

    for i in output['away_yellow_times']:
        ws.cell(row=(column_length), column=AY1).value = output['away_yellow_times'][j]
        AY1 += 1
        j += 1

    HR1 = 38
    j = 0

    for i in output['home_red_times']:
        ws.cell(row=(column_length), column=HR1).value = output['home_red_times'][j]
        HR1 += 1
        j += 1

    AR1 = 41
    j = 0

    for i in output['away_red_times']:
        ws.cell(row=(column_length), column=AR1).value = output['away_red_times'][j]
        AR1 += 1
        j += 1

    wb.save(file_path)

    print("{} - {} vs {} added.".format(output['date'], output['home_team_name'], output['away_team_name']))
