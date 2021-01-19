

# Undo Mechanic

class Move:
	# entity moves
	__slots__ = ('entity', 'dx', 'dy')

	def __init__(self,entity,dx,dy):
		self.entity = entity
		self.dx = dx
		self.dy = dy

	def undo(self):
		self.entity.move(-self.dx,-self.dy, trigger = False)

class ChangeStatus:
	# target tile or entity changes its status
	__slots__ = ('target', 'old_status', 'new_status')

	def __init__(self,target,old_status,new_status):
		self.target = target
		self.old_status = old_status
		self.new_status = new_status
		print("{} -> {}".format(self.old_status, self.new_status))
		self.target.update()

	def undo(self):
		#self.target.status = self.old_status
		self.target.change_status(self.old_status, save_change=False)
		print("{} -> {}".format(self.new_status, self.old_status))
		#self.target.update()

class Sink:
	__slots__ = ('sinker')

	def __init__(self,sinker):
		self.sinker = sinker

	def undo(self):
		sinker = self.sinker
		sinker.undo_sink()

class Transition:
	__slots__ = ('entity','dx','dy')

	def __init__(self,entity,dx,dy):
		self.entity = entity
		self.dx = dx
		self.dy = dy

	def undo(self):
		self.entity.transition(-self.dx,-self.dy, trigger=False)

class Possess:
	__slots__ = ('possessor', 'body')

	def __init__(self, possessor, body):
		self.possessor = possessor
		self.body = body

	def undo(self):
		self.body.depossess()

class Depossess:
	__slots__ = ('possessor', 'body')

	def __init__(self, possessor, body):
		self.possessor = possessor
		self.body = body

	def undo(self):
		self.possessor.possess(self.body)

"""
def undo(change):
	# Undo a change

	if isinstance(change, Move):
		# Get change data
		entity = change.entity
		dx = change.dx
		dy = change.dy
		# Undo move
	elif isinstance(change, ChangeStatus):
		# Get change data
		target = change.target
		old_status = change.old_status
		new_status = change.new_status
"""


# del move