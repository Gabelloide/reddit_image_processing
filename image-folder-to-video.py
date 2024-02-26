import os
import subprocess
import shutil
import tempfile
from time import perf_counter


def prepare_files(folder_path, temp_dir):
		"""Renaming each file to add a number readable by ffmpeg"""
		for i, filename in enumerate(os.listdir(folder_path)):
				shutil.copy(f'{folder_path}/{filename}', f'{temp_dir}/{i:04d}.png')


def create_video_from_images(temp_dir, output_file):
		command = ["ffmpeg", '-framerate', '15', '-i',
							 f'{temp_dir}/%04d.png', '-c:v', 'libx265', '-r', '15', '-pix_fmt', 'yuv420p', output_file]
		try:
				subprocess.run(command, check=True)
				print("Successfully created the video file.")
		except subprocess.CalledProcessError as e:
				print(f"An error occurred while processing the video file: {e}")


if __name__ == '__main__':
		folder_path = ''
		output_file = ''
		start_time = perf_counter()

		# Doing the work in a temporary directory
		with tempfile.TemporaryDirectory() as temp_dir:
				prepare_files(folder_path, temp_dir)
				create_video_from_images(temp_dir, output_file)

		end_time = perf_counter()
		execution_time = end_time - start_time
		print(f"Execution time: {round(execution_time, 2)} seconds")
