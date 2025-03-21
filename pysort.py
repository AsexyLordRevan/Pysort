import argparse
from PIL import Image
import numpy as np

# Define the color categories and their thresholds for classification
color_thresholds = {
    'red': [(150, 0, 0), (255, 100, 100)],
    'orange': [(200, 100, 0), (255, 165, 50)],
    'yellow': [(200, 200, 0), (255, 255, 100)],
    'green': [(0, 150, 0), (100, 255, 100)],
    'blue': [(0, 0, 150), (100, 100, 255)],
    'mauve': [(150, 50, 100), (255, 150, 200)],
    'white': [(200, 200, 200), (255, 255, 255)],
    'black': [(0, 0, 0), (50, 50, 50)],
}

# Function to classify pixels into color categories
def classify_color(r, g, b):
    """
    Classify an RGB color into a named color category based on predefined thresholds.
    
    This function checks if the given RGB values fall within the ranges defined in
    the color_thresholds dictionary. Each threshold consists of a lower and upper
    bound for the R, G, and B channels.
    
    Parameters:
    -----------
    r : int or float
        Red channel value
    g : int or float
        Green channel value
    b : int or float
        Blue channel value
    
    Returns:
    --------
    str or None
        The name of the color category if a match is found, otherwise None
    
    Notes:
    ------
    The function assumes that color_thresholds is a global dictionary with the format:
    {color_name: ((r_min, g_min, b_min), (r_max, g_max, b_max)), ...}
    """
    for color, (low, high) in color_thresholds.items():
        if low[0] <= r <= high[0] and low[1] <= g <= high[1] and low[2] <= b <= high[2]:
            return color
    return None

# Function to calculate average color for each category
def average_color(pixels, category):
    r_values = []
    g_values = []
    b_values = []
    
    for (r, g, b) in pixels:
        if classify_color(r, g, b) == category:
            r_values.append(r)
            g_values.append(g)
            b_values.append(b)
    
    if r_values:
        avg_r = np.mean(r_values)
        avg_g = np.mean(g_values)
        avg_b = np.mean(b_values)
        return (int(avg_r), int(avg_g), int(avg_b))
    else:
        return None  # Return None if no pixels were found for that category

# Function to generate ANSI escape codes for text color
def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

# Setup command-line argument parsing
def main():
    parser = argparse.ArgumentParser(description='Classify colors in an image and calculate average RGB values for each color category.')
    parser.add_argument('image_path', metavar='image', type=str, help='Path to the image file')
    
    # Parse arguments
    args = parser.parse_args()

    try:
        # Open the image
        image = Image.open(args.image_path)
        pixels = list(image.getdata())

        # Classify each pixel and calculate averages for each color category
        average_colors = {}
        for color in color_thresholds:
            avg_color = average_color(pixels, color)
            if avg_color is not None:  # Only store categories with pixels
                average_colors[color] = avg_color

        # Print the average colors in their respective categories
        print("\nAverage colors for each category:")
        block = '█' * 10
        for color, avg_color in average_colors.items():
            r, g, b = avg_color
            # Generate the ANSI color code for the text
            color_code = rgb_to_ansi(r, g, b)
            print(f"{color_code}{block} | Average {color} color: {avg_color}\033[0m")  # \033[0m resets the color to default
            # print block char for color

    except Exception as e:
        print(f"Error opening image: {e}")

if __name__ == "__main__":
    main()
