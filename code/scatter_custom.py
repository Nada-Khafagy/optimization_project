import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.transforms import Affine2D
from matplotlib.path import Path

# Create a custom rotated rectangle marker
def custom_marker(width, height, angle):
    # Define the path for a rotated rectangle
    vertices = [
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2),
        (-width / 2, -height / 2),  # Closed path
    ]
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    path = Path(vertices, codes)

    # Apply a rotation transformation to the path
    transform = Affine2D().rotate_deg(angle)
    rotated_path = path.transformed(transform)

    # Create a custom marker using the rotated path
    marker = MarkerStyle(marker=rotated_path)
    return marker


