import random

class Colour:
	@staticmethod
	def RAND_COLOUR():
		return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def constrain(value, max, min=0):
	if value <= min: return min
	elif value >= max: return max
	return value


def rect_collision(obj1, obj2):
	if obj1.position[0] in range(int(obj2.position[0] - obj2.size[0] // 2), int(obj2.position[0] + obj2.size[0] // 2)):           # requires radius ; 
			if obj1.position[1] in range(int(obj2.position[1] - obj2.size[1] // 2), int(obj2.position[1] + obj2.size[1] // 2)):	  # position in object
				return True
	return False

