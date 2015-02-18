"""Module to create the svg charts"""
import json
import pygal

# Temp data
with open('data-dump.json', 'r') as f:
    TEST_JSON = json.load(f)


class LineChartConfig(pygal.Config):
    """Customized configuration class for charts."""
    interpolate = 'hermite'
    interpolation_parameters = {'type': 'finite_difference'}
    width = 900
    height = 400
    show_only_major_dots = False
    show_dots = False
    legend_at_bottom = True
    fill = False
    pretty_print = True


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
    chart = pygal.Line(LineChartConfig())
    min_max_index = []

    for line in line_list:
        chart.add(line.name, line.data, secondary=line.secondary)

        # Index of min and max values for each line
        for i, j in enumerate(line.data):
            if j == min(line.data) or j == max(line.data):
                min_max_index.append(str(i))
        chart.x_labels = map(str, range(len(line.data)))

    # Mark min and max value dots
    chart.x_labels_major = min_max_index

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
        chart.render_to_file(file_name)

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
