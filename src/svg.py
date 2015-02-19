"""Module to create the svg charts"""
import json
import pygal

# Custom svg CSS style file
CUSTOM_SVG_CSS = '../web/assets/css/svg.css'

# Customized configuration class
chart_config = pygal.Config()
chart_config.interpolate = 'hermite'
chart_config.interpolation_parameters = {'type': 'finite_difference'}
chart_config.width = 900
chart_config.height = 400
chart_config.show_dots = True
chart_config.dots_size = 1
chart_config.legend_at_bottom = True
chart_config.fill = False
chart_config.pretty_print = True
chart_config.x_title = "Next 48 hours"
chart_config.show_x_labels = False
chart_config.show_y_labels = False
chart_config.tooltip_border_radius = 4
chart_config.tooltip_font_size = 12
chart_config.css.append(CUSTOM_SVG_CSS)

# Customized style class
chart_style = pygal.style.Style(
    background='transparent',
    plot_background='transparent'
    )


class Line(object):
    """Data about one line to be used when creating a line chart.

    Args:
        data_dict (dict): JSON weather data from Forecast.icon
        data_key (str): Name of weather value wanted out of data_dict
        time_frame (str): Time granularity of the JSON weather data.
        print_name (str): Display name for the weather value
        secondary (bool): Use secondary y axis?

    Atributes:
        self.data (list): Data points from the data_key in time_frame
            granularity.
        self.name (str): Key name of data points.
        self.print_name (str): Name to print on chart (defaults to name)
        self.secondary (bool): Use secondary y axis?
    """
    def __init__(self, data_dict, data_key, time_frame='hourly',
                 print_name=None, secondary=False):

        # Parse data_dict and assign list of data points to self.data
        try:
            data_block = data_dict[time_frame]['data']
        except IndexError:
            raise IndexError("Error. No weather data for %s time frame."
                             % time_frame)
        try:
            self.data = [chunk[data_key] for chunk in data_block]
        except IndexError:
            raise IndexError("Error. JSON data bock %s does not have %s key."
                             % (data_block, data_key))

        self.name = data_key
        if print_name:
            self.print_name = print_name
        else:
            self.print_name = self.name
        self.secondary = secondary


def create_chart(line_list):
    """Returns an pygal chart created from a list of Line objects."""
    chart = pygal.Line(chart_config, style=chart_style)
    min_max_index = []

    for line in line_list:
        chart.add(line.name, line.data, secondary=line.secondary)

        # Index of min and max values for each line
        for i, j in enumerate(line.data):
            if j == min(line.data) or j == max(line.data):
                min_max_index.append(str(i))
        # chart.x_labels = map(str, range(len(line.data)))

    # Mark min and max value dots
    # chart.x_labels_major = min_max_index

    return chart

if __name__ == '__main__':
    def save_svg(metrics):
        """For testing. Save svg to local file"""
        line_list = []
        file_name = ""
        for metric, sec_bool in metrics:
            line_list.append(Line(TEST_JSON, metric, secondary=sec_bool))
            file_name += metric + '-'
        chart = create_chart(line_list)
        file_name += 'chart.svg'
        chart.render_to_file("../web/assets/svg/" + file_name)

    # Test case 1 - % based metrics
    save_svg([('precipProbability', False), ('cloudCover', False)])

    # Test case 2 - 4 metrics
    save_svg([
        ('precipProbability', False),
        ('cloudCover', False),
        ('temperature', True),
        ('windSpeed', True)
        ])

    # Test case 3 - 2 different scales
    save_svg([('humidity', False), ('pressure', True)])
