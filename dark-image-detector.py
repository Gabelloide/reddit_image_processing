from PIL import Image


def evaluate_brightness(image_path):
		image = Image.open(image_path)
		image = image.convert('L')  # Convert to grayscale
		histogram = image.histogram()
		total_pixels = image.width * image.height

		# Count the number of pixels that are darker than 128
		dark_pixels = sum(histogram[:128])

		if dark_pixels / total_pixels > 0.5:
				return True  # Rather dark image
		elif dark_pixels / total_pixels < 0.5:
				return False  # Rather bright image
		else:  # Even
				return None


if __name__ == '__main__':

		import os

		# Path to the directory containing the images
		image_dir = r""

		# Create subdirectories for dark and light images
		dark_dir = os.path.join(image_dir, 'dark')
		light_dir = os.path.join(image_dir, 'light')
		os.makedirs(dark_dir, exist_ok=True)
		os.makedirs(light_dir, exist_ok=True)

		# Iterate over the images in the directory
		for filename in os.listdir(image_dir):
				if filename.endswith('.jpg') or filename.endswith('.png'):
						image_path = os.path.join(image_dir, filename)
						is_dark = evaluate_brightness(image_path)

						if is_dark is True:
								# Move the image to the dark directory
								new_path = os.path.join(dark_dir, filename)
								os.rename(image_path, new_path)
						elif is_dark is False:
								# Move the image to the light directory
								new_path = os.path.join(light_dir, filename)
								os.rename(image_path, new_path)
						else:
								# Do nothing if brightness cannot be determined
								pass
