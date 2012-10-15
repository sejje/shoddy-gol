import graphics
import random
from time import sleep


#Globals:
length = 20
pixels = 2

def create_window():
	#create the window we draw inside of
	window = graphics.GraphWin("Conway's Game of Life - Jesse Briggs", 500, 500)
	window.setCoords(0, 0, 60, 60)
	return window

def create_life_grid(length):
	#create an array that patterns a square with sides (length) long
	grid = [[0] * length for i in xrange(length)]
	return grid

def create_display_grid(length):
	#grid of points where rectangles are displayed
	#x, y of point 1, then x, y of point2 (pt1 and pt2 are opposite corners)
	grid = [[[pixels*i, pixels*j, pixels+pixels*i, pixels+pixels*j, None] for i in xrange(length)] for j in xrange(length)]
	return grid

def draw_window(window, display_grid, life_grid):
	#lookup each x, y from display in the life grid, find color and paint it
	x = 0
	y = 0
	for row in display_grid:
		for box in row:
			rec = graphics.Rectangle(graphics.Point(box[0], box[1]), graphics.Point(box[2], box[3]))
			color = life_grid[y][x]
			if color == 1:
				paint = "black"
			else:
				paint = "white"
			rec.setFill(paint)
			rec.draw(window)
			box[4] = rec
			y += 1
		y = 0
		x += 1

def update_display(display_grid, life_grid):
	#check for life in life_grid, set the fill accordingly in display_grid
	x = -1
	y = -1
	for row in life_grid:
		y += 1
		for item in row:
			x += 1
			if life_grid[y][x] == 1:
				display_grid[y][x][4].setFill("black")
			else:
				display_grid[y][x][4].setFill("white")
		x = -1
		
def iterate(life_grid):
	#print "iterate"
	#do one iteration of the rules on the life grid
	updated_grid = create_life_grid(length)
	for y in xrange(length):
		for x in xrange(length):
			count = count_neighbors_lame(y, x, life_grid)
			if life_grid[x][y] == 1:
				#checking live cell
				if count < 2 or count > 3:
					#a living cell died
					#print "living cell died at %s, %s" % (x, y)
					updated_grid[x][y] = 0
				if count == 2 or count == 3:
					updated_grid[x][y] = 1
			else:
				#checking dead cell
				if count == 3:
					#new life just spawned
					#print "life just spawned at %s, %s" % (x, y)
					updated_grid[x][y] = 1

	return updated_grid

def test_count(life_grid):
	return count_neighbors_lame(5, 5, life_grid)

def count_neighbors_lame(x, y, lg):
	count = 0
	try: count += lg[y+1][x] 
	except: pass
	try: count += lg[y-1][x] 
	except: pass
	try: count += lg[y][x+1] 
	except: pass
	try: count += lg[y+1][x+1] 
	except: pass
	try: count += lg[y-1][x+1] 
	except: pass
	try: count += lg[y][x-1] 
	except: pass
	try: count += lg[y+1][x-1] 
	except: pass
	try: count += lg[y-1][x-1] 
	except: pass
	return count

def count_neighbors(x, y, life_grid):
	count = 0
	for i in range(y-1, y+2):
		for j in range(x-1, x+2):
			if (y, x) == (i, j):
				break
			try:
				count += life_grid[i][j]
			except:
				pass
	return count

def seed_life(life_grid):
	#insert some life into the life grid, however you like (random?)
	for i in xrange(75):
		x = random.randrange(0, length - 1)
		y = random.randrange(0, length - 1)
		life_grid[x][y] = 1
	return life_grid

def main():
	#create window
	window = create_window()

	#create grid to show life
	life = create_life_grid(length)
	empty_life = create_life_grid(length)
	last_life = empty_life

	#create grid to hold rectangle info for drawing
	display = create_display_grid(length)

	#draw window
	draw_window(window, display, life)

	#populate some life into grid
	life = seed_life(life)
	update_display(display, life)

	#loop as long as there's life and it's not "stuck"
	while True:
		update_display(display, life)
		while not life == empty_life and not last_life == life:
			last_life = life
			life = iterate(life)
			update_display(display, life)
			sleep(.01)

		#start loop over
		window.getMouse()
		seed_life(life)

if __name__ == "__main__":
	main()
