import multiprocessing
import subprocess
import requests

def run_script(word):
	# Launch getReddit.py
	subprocess.run(["python", "getReddit.py", word])


if __name__ == '__main__':
  # Launch 10 processes that run getReddit.py with the word 'wallpaper'
	processes = []
	words = ['wallpaper'] * 10

	for word in words:
		p = multiprocessing.Process(target=run_script, args=(word,))
		processes.append(p)
		p.start()

	for p in processes:
		p.join()
