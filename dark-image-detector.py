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


# Example
image_path = r""
resultat = evaluate_brightness(image_path)
if resultat is True:
		print("This image is rather dark.")
elif resultat is False:
		print("This image is rather bright.")
else:
		print("This image is evenly lit.")
