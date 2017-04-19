assignments = []

diagonals = [ [ 'A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9' ] , [ 'A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1' ] ]

import collections

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
# print('boxes are {}'.format(boxes))
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# unitlist = row_units + column_units + square_units
unitlist = row_units + column_units + square_units + diagonals
# print('unitlist are {}'.format(unitlist))
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# print('units are {}'.format(units))
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# print('peers are {}'.format(peers))


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        length_2_boxes = [box for box in unit if len(values[box]) == 2]
        if len(length_2_boxes) > 1:
            # print('length_2_boxes are {}'.format(length_2_boxes))
            boxes_dict = {}
            for box in length_2_boxes:
                boxes_dict[box] = values[box]
            # print('boxes_dict are {}'.format(boxes_dict))
            duplicates = [item for item, count in collections.Counter(boxes_dict.values()).items() if count > 1]
            # print('duplicates are {}'.format(duplicates))
            # unit_dict = {}
            # for box in unit:
            #     unit_dict[box] = values[box]
            # print('unit_dict are {}'.format(unit_dict))
            for duplicate in duplicates:
                for box in unit:
                    for digit in duplicate:
                        if digit in values[box] and duplicate != values[box]:
                            # print('BOX BEFORE {}'.format(values[box]))
                            values[box] = values[box].replace(digit,'')
                            # print('BOX AFTER {}'.format(values[box]))
    return values


def check_diagonals(values):
    diagonals_dicts = []
    for diagonal in diagonals:
        diagonals_dict = {}
        for box in diagonal:
            diagonals_dict[box] = values[box]
        diagonals_dicts.append(diagonals_dict)
    # print('diagonal_dicts are {}'.format(diagonals_dicts))
    for diagonal_dictionary in diagonals_dicts:
        duplicates = [item for item, count in collections.Counter(diagonal_dictionary.values()).items() if count > 1]
        # print('diagonal duplicates are {}'.format(duplicates))
        if len(duplicates) > 0:
            return False
        else:
            return True





def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max( len(values[s]) for s in boxes )
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            # values[peer] = values[peer].replace(digit,'')
            replaced_box = values[peer].replace(digit,'')
            assign_value(values, peer, replaced_box)
    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, w = min( ( len(values[s]), s ) for s in boxes if len(values[s]) > 1 )

    # w = None
    # for s in boxes:
    #     length = len(values[s])
    #     if length > 1:
    #         # print('length is {}'.format(length))
    #         w = s
    #         # print('first one length > 1 is {}'.format(w))
    #         break
    # for s in boxes:
    #     length = len(values[s])
    #     if length > 1:
    #         if s < w:
    #             w = s
    # print('n is {}'.format(n))
    # print('w is {}'.format(w))

    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[w]:
        new_sudoku = values.copy()
        new_sudoku[w] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt




def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    final_values = search(values)
    check_diagonals(final_values)
    return final_values


# solved_diag_sudoku = {'G7': '8', 'G6': '9', 'G5': '7', 'G4': '3', 'G3': '2', 'G2': '4', 'G1': '6', 'G9': '5',
#                       'G8': '1', 'C9': '6', 'C8': '7', 'C3': '1', 'C2': '9', 'C1': '4', 'C7': '5', 'C6': '3',
#                       'C5': '2', 'C4': '8', 'E5': '9', 'E4': '1', 'F1': '1', 'F2': '2', 'F3': '9', 'F4': '6',
#                       'F5': '5', 'F6': '7', 'F7': '4', 'F8': '3', 'F9': '8', 'B4': '7', 'B5': '1', 'B6': '6',
#                       'B7': '2', 'B1': '8', 'B2': '5', 'B3': '3', 'B8': '4', 'B9': '9', 'I9': '3', 'I8': '2',
#                       'I1': '7', 'I3': '8', 'I2': '1', 'I5': '6', 'I4': '5', 'I7': '9', 'I6': '4', 'A1': '2',
#                       'A3': '7', 'A2': '6', 'E9': '7', 'A4': '9', 'A7': '3', 'A6': '5', 'A9': '1', 'A8': '8',
#                       'E7': '6', 'E6': '2', 'E1': '3', 'E3': '4', 'E2': '8', 'E8': '5', 'A5': '4', 'H8': '6',
#                       'H9': '4', 'H2': '3', 'H3': '5', 'H1': '9', 'H6': '1', 'H7': '7', 'H4': '2', 'H5': '8',
#                       'D8': '9', 'D9': '2', 'D6': '8', 'D7': '1', 'D4': '4', 'D5': '3', 'D2': '7', 'D3': '6',
#                       'D1': '5'}



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    # display(solved_diag_sudoku)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
