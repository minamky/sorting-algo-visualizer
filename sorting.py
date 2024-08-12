import pygame
import random
import math
import time
pygame.init()

class DrawInformation:
	BLACK = 0, 0, 0
	DARK_RED = (219, 7, 61)
	LIGHT_RED = (233, 87, 95)
	WHITE = 255, 255, 255
	GREEN = (150, 237, 137)
	BLUE = 173, 213, 247

	BACKGROUND_COLOR = (255, 233, 231)

	GRADIENT = [
		(254, 188, 185),
		(251, 165, 163),
		(246, 142, 141)
	]

	FONT = pygame.font.SysFont('arial', 15)
	MEDIUM_FONT = pygame.font.SysFont('arial', 20)
	LARGE_FONT = pygame.font.SysFont('arial', 30)

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending, n, speed):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} ~ {'Ascending' if ascending else 'Descending'}", 1, draw_info.DARK_RED)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	speed_math = 100 - round(speed * 1000)
	speed = draw_info.MEDIUM_FONT.render(f"Number of Blocks: {n} | Speed: {speed_math}%", 1, draw_info.DARK_RED)
	draw_info.window.blit(speed, (draw_info.width/2 - speed.get_width()/2, 35))

	num_blocks = draw_info.FONT.render("↑ More Blocks | ↓ Less Blocks | → Faster | ← Slower", 1, draw_info.LIGHT_RED)
	draw_info.window.blit(num_blocks, (draw_info.width/2 - num_blocks.get_width()/2, 60))

	sorting = draw_info.FONT.render("I - Insert Sort | B - Bubble Sort | Q - Quick Sort", 1, draw_info.LIGHT_RED)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 80))

	ascending = draw_info.FONT.render("A - Ascending | D - Descending", 1, draw_info.LIGHT_RED)
	draw_info.window.blit(ascending, (draw_info.width/2 - ascending.get_width()/2, 100))

	controls = draw_info.FONT.render("R - Reset | SPACE - Begin Sorting", 1, draw_info.LIGHT_RED)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 120))

	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, 
			draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENT[i % 3]

		if i in color_positions:
			color = color_positions[i]

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()

def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst

def bubble_sort(draw_info, ascending=True, speed = 0.0):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j+1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j+1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.BLUE}, True)
				yield True
				time.sleep(speed)
	return lst

def insert_sort(draw_info, ascending=True, speed = 0.0):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		key = lst[i]
		j = i - 1

		while ((ascending and j >= 0 and key < lst[j]) or (not ascending and j>=0 and key > lst[j])):
			lst[j + 1] = lst[j]
			j -= 1
			draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.BLUE}, True)
			time.sleep(speed)
			yield True

		lst[j + 1] = key
		time.sleep(speed)
		yield True

	return lst

def partition(arr, low, high, ascending):
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if (arr[j] < pivot and ascending) or (arr[j] > pivot and not ascending):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(draw_info, ascending=True, speed = 0.0):
	lst = draw_info.lst
	yield from quick_sort_helper(draw_info, lst, 0, len(lst) - 1, ascending, speed)


def quick_sort_helper(draw_info, arr, low, high,ascending, speed):
    if low < high:
        pi = partition(arr, low, high, ascending)

        draw_list(draw_info, {i: draw_info.GREEN for i in range(low, pi)}, True)
        yield True
        time.sleep(speed)

        draw_list(draw_info, {i: draw_info.GREEN for i in range(pi + 1, high + 1)}, True)
        yield True
        time.sleep(speed)

        yield from quick_sort_helper(draw_info, arr, low, pi - 1, ascending, speed)
        yield from quick_sort_helper(draw_info, arr, pi + 1, high, ascending, speed)


def main():
    run = True
    clock = pygame.time.Clock()

    sorting = False
    ascending = True

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    n = 50
    min_val = 0
    max_val = 100
    speed = 0.05

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)


    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
                sorting_algo_generator = None
        else:
            draw(draw_info, sorting_algo_name, ascending, n, speed)

        for event in pygame.event.get():
        	if event.type == pygame.QUIT:
        		run = False

        	if event.type != pygame.KEYDOWN:
        		continue

        	# reset
        	if event.key == pygame.K_r:
        		lst = generate_starting_list(n, min_val, max_val)
        		draw_info.set_list(lst)
        		sorting = False

        	# start
        	elif event.key == pygame.K_SPACE and not sorting:
        		sorting = True
        		sorting_algo_generator = sorting_algo(draw_info, ascending, speed)

        	# ascending or descending
        	elif event.key == pygame.K_a and not sorting:
        		ascending = True
        	elif event.key == pygame.K_d and not sorting:
        		ascending = False

        	# choosing sort algo
        	elif event.key == pygame.K_i and not sorting:
        		sorting_algo = insert_sort
        		sorting_algo_name = "Insertion Sort"
        	elif event.key == pygame.K_b and not sorting:
        		sorting_algo = bubble_sort
        		sorting_algo_name = "Bubble Sort"
        	elif event.key == pygame.K_q and not sorting:
        		sorting_algo = quick_sort
        		sorting_algo_name = "Quick Sort"

        	# adjust number of bars
        	elif event.key == pygame.K_UP and not sorting:
        		n = min(n + 10, 200)
        		lst = generate_starting_list(n, min_val, max_val)
        		draw_info.set_list(lst)
        	elif event.key == pygame.K_DOWN and not sorting:
        		n = max(n - 10, 10)
        		lst = generate_starting_list(n, min_val, max_val)
        		draw_info.set_list(lst)

        	# increase and decrease speed
        	elif event.key == pygame.K_RIGHT and not sorting:
        		speed = max(speed - 0.01, 0.00) 
        	elif event.key == pygame.K_LEFT and not sorting:
        		speed = min(speed + 0.01, 0.09)


    pygame.quit()

if __name__ == "__main__":
    main()