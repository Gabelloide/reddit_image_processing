from multiprocessing import Pool
from PIL import Image, ImageFile
import os
import time


ImageFile.LOAD_TRUNCATED_IMAGES = True
def convert_images(folder_path, batch):
	count = 0
	for filename in batch:
		if filename.endswith('.jpg') or filename.endswith('.jpeg'):
			try:
				img = Image.open(f'{folder_path}/{filename}')
				img.save(f'{folder_path}/{filename[:-4]}.png')
				img.close()
				os.remove(f'{folder_path}/{filename}')
				count += 1  # +1 if image is converted
			except OSError:
				print(f"Cannot convert {filename}. The image file is truncated.")
	return count


def jpg_to_png(folder_path):
	"""Convert jpg/jpeg images to png"""
	count = 0
	batch_size = 83
	image_files = os.listdir(folder_path)
	batches = [image_files[i:i+batch_size] for i in range(0, len(image_files), batch_size)]
	with Pool() as p:
		count += sum(p.starmap(convert_images, [(folder_path, batch) for batch in batches]))
	return count


if __name__ == '__main__':
	try:
		folder_path = r''
		start_time = time.perf_counter()
		converted_count = jpg_to_png(folder_path)
		end_time = time.perf_counter()
		execution_time = end_time - start_time
		print(f"Execution time: {round(execution_time, 2)} seconds")
		print(f"Number of images converted: {converted_count}")
	except Exception as e:
		print(f"Error: {e}")
