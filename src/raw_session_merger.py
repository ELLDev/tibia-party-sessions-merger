class Session:
    def __init__(self, players, players_balance, total_balance, party_size):
        self.players = players
        self.players_balance = players_balance
        self.total_balance = total_balance
        self.party_size = party_size
        self.payroll = {}


def format_raw_party_session_data(list_text):
    session = Session([], [], 0, 0)

    for current_line in range(len(list_text)):
        if ":" not in list_text[current_line] and len(list_text[current_line]) > 0:
            can_remove_commas = True
            session.party_size += 1
            player_name = list_text[current_line]
            if "(" in player_name:
                bracket_index = player_name.index("(")
                player_name = player_name[:bracket_index - 1]
            session.players.append(player_name)

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
            session.total_balance += player_balance
            session.players_balance.append((player_name, player_balance))

    return session


def split_loot(session):
    profit_per_player = int((session.total_balance / session.party_size) / 100) * 100

    player_debt = {key: 0 for key in session.players}
    debt_correspondence = {key: [] for key in session.players}
    for player in session.players_balance:
        if player[1] > profit_per_player:
            player_debt[player[0]] = player[1] - profit_per_player
        else:
            player_debt[player[0]] = player[1] - profit_per_player

    while True:
        highest_debt_player = max(player_debt, key=player_debt.get)
        lowest_debt_player = min(player_debt, key=player_debt.get)

        if player_debt[highest_debt_player] <= (session.party_size - 1) * 100:
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

    return debt_correspondence


def merge_sessions_payroll(sessions):
    payroll = {}
    for session in sessions:
        for key in session.payroll:
            if key not in payroll:
                payroll[key] = session.payroll[key]
            else:
                if len(session.payroll[key]) > 0 and len(payroll[key]) == 0:
                    payroll[key] += session.payroll[key]
                else:
                    if len(session.payroll[key]) > 0:
                        for debt in range(len(session.payroll[key])):
                            for debt_ in range(len(payroll[key])):
                                if payroll[key][debt_][0] == session.payroll[key][debt][0]:
                                    payroll[key][debt_][1] += session.payroll[key][debt][1]
                                    break
                                if debt_ == len(payroll[key]) - 1:
                                    payroll[key].append(session.payroll[key][debt])
    return payroll


def merge_raw_session_logs(input_data):
    output = ""
    session_instances = []
    party_sessions_index = []

    sessions = list(input_data.split("\n"))
    for current_line in range(len(sessions)):
        if "Session data:" in sessions[current_line]:
            party_sessions_index.append(current_line)
    party_sessions_index.append(len(sessions))  # add "end" index for the last session

    for i in range(len(party_sessions_index) - 1):
        start = party_sessions_index[i]
        end = party_sessions_index[i + 1]
        session_instances.append(format_raw_party_session_data(sessions[start:end - 1]))

    for session in session_instances:
        session.payroll = split_loot(session)

    payroll = merge_sessions_payroll(session_instances)

    for debt in payroll:
        if len(payroll[debt]) > 0:
            output += (debt + ":" + "\n")
            for entry in payroll[debt]:
                output += ("    transfer " + str(entry[1]) + " to " + entry[0] + "\n")

    return output
