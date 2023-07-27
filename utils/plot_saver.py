import matplotlib.pyplot as plt
import config

class PlotSaver:
    def __init__(self, plot_object, input_name):
        self.plot_object = plot_object
        self.input_name = input_name

    def save_plot(self, x_label, y_label, plot_title):
        # Generate the plot
        plt.figure()
        self.plot_object()

        # Set labels and title
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(plot_title)

        # Save the plot to the specified path
        save_path = config.PLOT_SAVE_PATH  # Assuming you have a PLOT_SAVE_PATH defined in config.py
        file_name = f"{self.input_name}.png"
        save_file = save_path + file_name
        plt.savefig(save_file)
        print(f"Plot saved successfully at: {save_file}")
