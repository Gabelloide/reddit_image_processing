from multiprocessing import Pool
from PIL import Image
import os
import time


def convert_image(args):
		folder_path, filename = args
		if filename.endswith('.jpg'):
				img = Image.open(f'{folder_path}/{filename}')
				img.save(f'{folder_path}/{filename[:-4]}.png')
				os.remove(f'{folder_path}/{filename}')
				return 1  # +1 if image is converted
		return 0


def jpg_to_png(folder_path):
		"""Convert jpg/jpeg images to png"""
		count = 0  # Initialize the count
		with Pool() as p:
				count += sum(p.map(convert_image, [(folder_path, filename)
																					 for filename in os.listdir(folder_path)]))
		return count

if __name__ == '__main__':
		folder_path = ''
		start_time = time.perf_counter()
		converted_count = jpg_to_png(folder_path)
		end_time = time.perf_counter()
		execution_time = end_time - start_time
		print(f"Execution time: {round(execution_time, 2)} seconds")
		print(f"Number of images converted: {converted_count}")
