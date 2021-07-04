def format_tibiapal_party_log(input_text):
    list_text = list(input_text.split("\n"))
    formatted_text = []
    debt_players = []
    players_balance = []
    output = ""

    for current_line in list_text:
        if len(current_line) > 0 and "pay" in current_line:
            debt_player_name_index = current_line.index("to pay")
            debt_player_name = current_line[:debt_player_name_index - 1]

            trim_index = current_line.index("transfer")
            current_line = current_line[trim_index + 9:len(current_line) - 1]
            trim_index = current_line.index("to")
            current_line = current_line[trim_index + 3:] + "." + current_line[:trim_index - 1] + "," + debt_player_name
            formatted_text.append(current_line)

    for entry in formatted_text:
        tmp_list = []
        player_name_trim_index = entry.index(".")
        debt_player_name_trim_index = entry.index(",")

        player_name = entry[:player_name_trim_index]
        debt = int(entry[player_name_trim_index + 1:debt_player_name_trim_index])
        debt = int(debt / 100) * 100
        debt_player_name = entry[debt_player_name_trim_index + 1:]
        debt_players.append(debt_player_name)
        tmp_list.append(player_name)
        tmp_list.append(debt)
        players_balance.append((tmp_list, debt_player_name))

    my_dict = {key: [] for key in debt_players}
    for t in players_balance:
        my_dict[t[1]].append(t[0])

    for debt in my_dict:
        output += (debt + ":" + "\n")
        for entry in my_dict[debt]:
            output += ("    transfer " + str(entry[1]) + " to " + entry[0] + "\n")

    return output
