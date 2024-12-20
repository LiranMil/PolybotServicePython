from pathlib import Path
from matplotlib.image import imread, imsave
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):
        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j - 1] - row[j]))

            self.data[i] = res

    def rotate(self):
        """
        Rotate the image 90 degrees clockwise.
        """
        height = len(self.data)
        width = len(self.data[0])

        rotated = []
        for col in range(width):
            new_row = []
            for row in reversed(self.data):
                new_row.append(row[col])
            rotated.append(new_row)

        self.data = rotated

    def salt_n_pepper(self):
        """
        Adds salt and pepper noise to the image.
        """
        height = len(self.data)
        width = len(self.data[0])

        for i in range(height):
            for j in range(width):
                rand_val = random.random()
                if rand_val < 0.2:
                    self.data[i][j] = 255  # Salt (white)
                elif rand_val > 0.8:
                    self.data[i][j] = 0  # Pepper (black)

    def concat(self, other_img, direction='horizontal'):
        """
        Concatenates the image with another image either horizontally or vertically.
        """
        if direction == 'horizontal' and len(self.data) != len(other_img.data):
            raise RuntimeError("Images have different heights and cannot be concatenated horizontally.")

        if direction == 'vertical' and len(self.data[0]) != len(other_img.data[0]):
            raise RuntimeError("Images have different widths and cannot be concatenated vertically.")

        if direction == 'horizontal':
            for i in range(len(self.data)):
                self.data[i] += other_img.data[i]
        elif direction == 'vertical':
            self.data += other_img.data

    def segment(self):
        """
        Segments the image by converting pixels with intensity > 100 to white (255),
        and pixels with intensity <= 100 to black (0).
        """
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] > 100:
                    self.data[i][j] = 255  # White
                else:
                    self.data[i][j] = 0  # Black
