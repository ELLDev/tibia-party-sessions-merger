def format_raw_party_session_data(session_data):
    list_text = list(session_data.split("\n"))
    players = []
    players_balance = []
    party_size = 0
    total_balance = 0

    for current_line in range(len(list_text)):
        if ":" not in list_text[current_line] and len(list_text[current_line]) > 0:
            party_size += 1
            player_name = list_text[current_line]
            if "(" in player_name:
                bracket_index = player_name.index("(")
                player_name = player_name[:bracket_index - 1]
            players.append(player_name)

            player_balance = list_text[current_line + 3]
            colon_index = player_balance.index(":")
            comma_index = player_balance.index(",")
            player_balance = int(player_balance[colon_index + 2:comma_index] + player_balance[comma_index + 1:])
            total_balance += player_balance
            players_balance.append((player_name, player_balance))

    return players, players_balance, total_balance, party_size
