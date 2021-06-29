def format_raw_party_session_data(session_data):
    list_text = list(session_data.split("\n"))
    players = []
    players_balance = []
    party_size = 0
    total_balance = 0

    for current_line in range(len(list_text)):
        if ":" not in list_text[current_line] and len(list_text[current_line]) > 0:
            can_remove_commas = True
            party_size += 1
            player_name = list_text[current_line]
            if "(" in player_name:
                bracket_index = player_name.index("(")
                player_name = player_name[:bracket_index - 1]
            players.append(player_name)

            player_balance = list_text[current_line + 3]
            colon_index = player_balance.index(":")
            player_balance = player_balance[colon_index + 2] + player_balance[colon_index + 3:]
            while can_remove_commas:
                try:
                    comma_index = player_balance.index(",")
                    player_balance = player_balance[:comma_index] + player_balance[comma_index + 1:]
                except ValueError:
                    can_remove_commas = False

            player_balance = int(player_balance)
            player_balance = int(player_balance / 100) * 100
            total_balance += player_balance
            players_balance.append((player_name, player_balance))

    return players, players_balance, total_balance, party_size


def split_loot(players, players_balance, total_balance, party_size):
    profit_per_player = int((total_balance / party_size) / 100) * 100

    player_debt = {key: 0 for key in players}
    debt_correspondence = {key: [] for key in players}
    for player in players_balance:
        if player[1] > profit_per_player:
            player_debt[player[0]] = player[1] - profit_per_player
        else:
            player_debt[player[0]] = player[1] - profit_per_player

    while True:
        highest_debt_player = max(player_debt, key=player_debt.get)
        lowest_debt_player = min(player_debt, key=player_debt.get)

        if player_debt[highest_debt_player] <= (party_size - 1) * 100:
            break

        if abs(player_debt[highest_debt_player]) > abs(player_debt[lowest_debt_player]):
            player_debt[highest_debt_player] += player_debt[lowest_debt_player]
            debt = [lowest_debt_player, abs(player_debt[lowest_debt_player])]
            debt_correspondence[highest_debt_player].append(debt)
            player_debt[lowest_debt_player] = 0

        else:
            player_debt[lowest_debt_player] += player_debt[highest_debt_player]
            debt = [lowest_debt_player, abs(player_debt[highest_debt_player])]
            debt_correspondence[highest_debt_player].append(debt)
            player_debt[highest_debt_player] = 0

    output = ""
    for debt in debt_correspondence:
        if len(debt_correspondence[debt]) > 0:
            output += (debt + ":" + "\n")
            for entry in debt_correspondence[debt]:
                output += ("    transfer " + str(entry[1]) + " to " + entry[0] + "\n")
    return output
