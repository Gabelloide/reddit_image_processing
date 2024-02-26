from multiprocessing import Pool
import os
import threading
from PIL import Image
import time

def evaluate_brightness(image_path, threshold):
	if not 0 < threshold < 1:
		raise ValueError("Threshold must be between 0 and 1")
	image = Image.open(image_path)
	if image.mode == 'P':
		image = image.convert('RGBA')  # Convert to ARGB to prevent warnings
	image = image.convert('L')  # Convert to grayscale
	histogram = image.histogram()
	total_pixels = image.width * image.height

	# Count the number of pixels that are darker than 128
	dark_pixels = sum(histogram[:128])

	if dark_pixels / total_pixels >= threshold:
		return True  # Rather dark image
	elif dark_pixels / total_pixels < threshold:
		return False  # Rather bright image

def process_batch(batch, threshold):
	for filename in batch:
		image_path = os.path.join(image_dir, filename)
		is_dark = evaluate_brightness(image_path, threshold)

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


# Input directory
image_dir = r""
# Subdirectories for dark and light images
dark_dir = os.path.join(image_dir, 'dark')
light_dir = os.path.join(image_dir, 'light')
os.makedirs(dark_dir, exist_ok=True)
os.makedirs(light_dir, exist_ok=True)

if __name__ == '__main__':
	start_time = time.perf_counter()

	# Define the number of images per batch
	images_per_batch = 83
	threshold = 0.9

	# Get the list of image files
	image_files = [filename for filename in os.listdir(
		image_dir) if filename.endswith('.jpg') or filename.endswith('.png')]

	# Split the image files into batches
	image_batches = [image_files[i:i+images_per_batch]
					for i in range(0, len(image_files), images_per_batch)]

	print(f"{len(image_batches)} batches created")
	# ---------- Threading approach ----------
	threads = []
	for batch in image_batches:
		thread = threading.Thread(target=process_batch, args=(batch,threshold))
		thread.start()
		threads.append(thread)

	# Wait for all threads to complete
	for thread in threads:
		thread.join()

	# ---------- Mutliprocessing approach ----------
	# with Pool(12) as p:  # Create a pool of 12 processes
	# 	p.map(process_batch, [batch for batch in image_batches])

	end_time = time.perf_counter()
	print(f"Execution time: {end_time - start_time} seconds")
