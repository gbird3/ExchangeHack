# Genetic Algorithm

class Solution(object):

	def __init__(self):
		self.room = None
		self.start = None
		self.end = None
		self.time = None # length of the class in hrs
		self.course = None
		self.section = None
		self.num_students = None
		self.pref_room_type = None
		self.pref_time = None


	def get_fitness(self):
		'''calculates the fitness function 
		for the current time slot'''
		pass

	def crossover(self):
		'''crosses with another solution 
		and returns a new solution'''
		pass

	def mutate(self):
		'''mutates the solution in some way'''
		print('please be more vague')


if __name__ == '__main__':
	print('this is dumb.')