def format_tibiapal_party_log(input_text):
    list_text = list(input_text.split("\n"))
    formatted_text = []
    players = []
    players_balance = []
    output = ""

    for current_line in list_text:
        if len(current_line) > 0 and "pay" in current_line:
            trim_index = current_line.index("transfer")
            current_line = current_line[trim_index + 9:len(current_line) - 1]
            trim_index = current_line.index("to")
            current_line = current_line[trim_index + 3:] + " " + current_line[:trim_index]
            formatted_text.append(current_line)

    for i in formatted_text:
        for char in i:
            if char.isdigit():
                digit_trim_index = i.index(char)
                break
        j = i[:digit_trim_index - 1]
        i = i[digit_trim_index:]
        players.append(j)
        players_balance.append((j, int(i)))

    my_dict = {key: 0 for key in players}
    for t in players_balance:
        my_dict[t[0]] += t[1]

    for key in my_dict:
        output = output + ("transfer " + str(int(my_dict[key] / 1000) * 1000) + " to " + key + "\n")
    return output
