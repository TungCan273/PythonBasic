
def flip_cap(number_of_cap, cap_status):
    """
    :param number_of_cap: integer, the number of cap in the line.
    :param cap_status: string, the status of each caps in the line respectively.
    :return: a list containing pair of the start and end position of the group needed to flip cap.
    """
    last_cap_status = '#'
    first_position = [0 for i in range(int(number_of_cap))]

    count_forward_group = 0
    count_backward_group = 0

    for i in range(int(number_of_cap)):
        if cap_status[i] == 'H':
            last_cap_status = cap_status[i]
            continue
        if cap_status[i] == last_cap_status:
            first_position[i] = first_position[i - 1]
            continue
        first_position[i] = i
        last_cap_status = cap_status[i]
        if cap_status[i] == 'F':
            count_forward_group += 1
        else:
            count_backward_group += 1

    # Determine which type of hat status need to be flipped
    cap_need_to_flip = 'B' if (count_backward_group < count_forward_group) else 'F'

    flipping_list = []
    last_cap_status = '#'
    for i in range(int(number_of_cap) - 1, -1, -1):
        if cap_status[i] == cap_need_to_flip and cap_status[i] != last_cap_status:
            flipping_list.append((first_position[i], i))
        last_cap_status = cap_status[i]

    # Reverse the list to print the result in ascending order
    flipping_list = flipping_list[::-1]

    return flipping_list


if __name__ == "__main__":
    number_of_cap = input('Enter the number of people: ')
    cap_status = input(f'Enter hat status of {number_of_cap} people: ')

    flipping_list = flip_cap(number_of_cap, cap_status)

    # Print the result
    for flipping_pair in flipping_list:
        start_index = flipping_pair[0]
        end_index = flipping_pair[1]
        if start_index == end_index:
            print(f'Person at position {start_index} please flip your cap!')
        else:
            print(f'People in positions {start_index} through {end_index} flip your cap!')
