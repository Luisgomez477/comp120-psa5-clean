"""
Module: supplies_visualizer

An application to visualize the result of the Distaster Planning problem.

DO NOT MODIFY THIS FILE IN ANY WAY!!!!!

Author(s):
1. Dr. Sat Garcia (sat@sandiego.edu)

"""

import PySimpleGUI as sg
import os

from supplies import parse_network_data, can_be_disaster_ready

LOC_SIZE = 50  # number of pixels in a single "square" (i.e. location) in our map
MAP_WIDTH = 12
MAP_HEIGHT = 10

def create_circle(x, y, r, target_canvas):
    """Draws a circle centered at (x,y) with radius r on the given canvas."""
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return target_canvas.TKCanvas.create_oval(x0, y0, x1, y1, outline='black',
                                              width=2)

def get_city_abbreviation(city_name):
    """Comes up with an abbreviation for a city name."""
    words = city_name.split()
    if len(city_name) < 3:
        return city_name
    elif len(words) == 1:
        return city_name[:3]
    else:
        return "".join([w[0] for w in words])

def draw_connections(network, locations, target_canvas):
    """Draws the lines connecting cities at the given locations in the road
    network."""
    for city, neighbors in network.items():
        c_x, c_y = locations[city]

        for n in neighbors:
            n_x, n_y = locations[n]

            start_x = c_x*LOC_SIZE + LOC_SIZE//2
            end_x = n_x*LOC_SIZE + LOC_SIZE//2
            start_y = c_y*LOC_SIZE + LOC_SIZE//2
            end_y = n_y*LOC_SIZE + LOC_SIZE//2

            target_canvas.TKCanvas.create_line(start_x, start_y, end_x, end_y,
                                               fill='black', width=2)

def draw_cities(locations, supply_locations, target_canvas):
    """Draws the cities at the given locations, coloring them white if they
    are not a supply location and green if they are a supply location."""

    for city, loc in locations.items():
        x, y = loc

        # determine the center of the city on the canvas
        center_x = x*LOC_SIZE + LOC_SIZE//2
        center_y = y*LOC_SIZE + LOC_SIZE//2

        cir = create_circle(center_x, center_y, 20, target_canvas)
        is_supply_city = city in supply_locations

        # color based on whether its a supply city
        if is_supply_city:
            target_canvas.TKCanvas.itemconfig(cir, fill="#608000")
        else:
            target_canvas.TKCanvas.itemconfig(cir, fill="White")

        text_color = "White" if is_supply_city else "Black"
        city_text = target_canvas.TKCanvas.create_text(center_x, center_y,
                                                       anchor="center", fill=text_color)
        target_canvas.TKCanvas.itemconfig(city_text, text=get_city_abbreviation(city))


def get_min_solution(network):
    """Determines the minimum number of cities needed to be disaster ready."""
    supply_cities = set()
    i = 0
    while i < len(network) and (not can_be_disaster_ready(network, i, supply_cities)):
        i += 1
        supply_cities.clear()

    return supply_cities


def solve(dst_filename, canvas):
    """Solves the disaster planning problem for the cities found in
    <dst_filename> and draws them on the canvas."""

    canvas.TKCanvas.delete('all')

    network, locations = parse_network_data(f'data_files/{dst_filename}')
    supply_cities = get_min_solution(network)

    draw_connections(network, locations, canvas)
    draw_cities(locations, supply_cities, canvas)


def main():
    # get list of ".dst" files in the data_files directory, sorted by name
    dst_files = [each for each in os.listdir('data_files') if each.endswith('.dst')]
    dst_files.sort()

    # create the GUI window layout
    sg.theme('Purple')
    layout = [
        [sg.Canvas(size=(MAP_WIDTH*LOC_SIZE, MAP_HEIGHT*LOC_SIZE), key='canvas')],
        [sg.Combo(dst_files, default_value=dst_files[0], enable_events=True, readonly=True, k='-FILE-'),
         sg.Button('Solve', k='-SOLVE-')]
    ]

    window = sg.Window('Disaster Planning (COMP120)', layout, finalize=True,
                       element_justification='c')
    canvas = window['canvas']

    solve(dst_files[0], canvas)

    # event loop to respond to closing the window or selecting a new file to
    # solve
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-SOLVE-':
            solve(values['-FILE-'], canvas)

if __name__ == "__main__":
    main()
