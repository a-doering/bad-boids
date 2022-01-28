import random
import yaml
from numpy import array
random.seed(42)
config = yaml.safe_load(open("config.yaml"))

class Boids:
	def __init__(self,
		count,
		x_range,
		y_range,
		xv_range,
		yv_range,
		flock_attraction,
		avoidance_radius,
		formation_flying_radius,
		speed_matching
		):
		#TODO: decouple the creation of boids from the updating
		self.count = count
		self.x_range = x_range
		self.y_range = y_range
		self.xv_range = xv_range
		self.yv_range = yv_range
		self.flock_attraction = flock_attraction
		self.avoidance_radius = avoidance_radius
		self.formation_flying_radius = formation_flying_radius
		self.speed_matching = speed_matching

	def initialize_boids(self):
		self.boids = [
			Boid(
				random.uniform(*self.x_range),
				random.uniform(*self.y_range),
				random.uniform(*self.xv_range),
				random.uniform(*self.yv_range),
				self
			)
			for boid in range(self.count)
		]


	def initialize_from_data(self, data):
		self.boids = [Boid(x, y, xv, yv, self) for x, y, xv, yv in zip(*data)]


	def update_boids(self):

		for me in self.boids:
			for other in self.boids:
				me.interact_1(other)
		for me in self.boids:
			for other in self.boids:
				me.interact_2(other)				
		for me in self.boids:
			me.position += me.velocity

		# def move(xs,ys,xvs,yvs):
		# 	# Move according to velocities
		# 	num_boids = len(xs)
		# 	for i in range(num_boids):
		# 		xs[i]+=xvs[i]
		# 		ys[i]+=yvs[i]

class Boid:
	def __init__(self,x,y,xv,yv,flock):
		self.position = array([x,y])
		self.velocity = array([xv,yv])
		self.flock = flock

	
	def interact_1(self, other):
		separation = other.position - self.position
		# Fly to middle
		self.velocity += separation*self.flock.flock_attraction / self.flock.count
		# # Fly away from nearby boids
		if separation.dot(separation) < self.flock.avoidance_radius**2:
			self.velocity -= separation

		# x_separation = (xs[j]-xs[i])
		# y_separation = (ys[j]-ys[i])
		# xvs[i]+=x_separation*config["boids"]["flock_attraction"]/num_boids
		# yvs[i]+=y_separation*config["boids"]["flock_attraction"]/num_boids
		# if x_separation**2 + y_separation**2 < config["boids"]["avoidance_radius"]**2:
		# 	xvs[i]-=x_separation
		# 	yvs[i]-=y_separation		
	def interact_2(self, other):
		separation = other.position - self.position
		if separation.dot(separation) < self.flock.formation_flying_radius**2:
			self.velocity += (other.velocity-self.velocity)*self.flock.speed_matching /self.flock.count
		# x_separation = (xs[j]-xs[i])
		# y_separation = (ys[j]-ys[i])
		# if x_separation**2 + y_separation**2 < config["boids"]["formation_flying_radius"]**2:
		# 	xvs[i]+=(xvs[j]-xvs[i])*config["boids"]["speed_matching"]/num_boids
		# 	yvs[i]+=(yvs[j]-yvs[i])*config["boids"]["speed_matching"]/num_boids

def init_boids():
	boids_x=[random.uniform(*config["boids"]["x"]) for x in range(config["boids"]["num"])]
	boids_y=[random.uniform(*config["boids"]["y"]) for x in range(config["boids"]["num"])]
	boid_x_velocities=[random.uniform(*config["boids"]["xv"]) for x in range(config["boids"]["num"])]
	boid_y_velocities=[random.uniform(*config["boids"]["yv"]) for x in range(config["boids"]["num"])]
	boids=(boids_x,boids_y,boid_x_velocities,boid_y_velocities)
	return boids

def update_boids(boids):
	xs,ys,xvs,yvs=boids
	adjust_velocity(xs,ys,xvs,yvs)
	move(xs,ys,xvs,yvs)

def adjust_velocity(xs,ys,xvs,yvs):
	num_boids = len(xs)
	# Fly towards the middle
	for i in range(num_boids):
		for j in range(num_boids):
			x_separation = (xs[j]-xs[i])
			y_separation = (ys[j]-ys[i])
			xvs[i]+=x_separation*config["boids"]["flock_attraction"]/num_boids
			yvs[i]+=y_separation*config["boids"]["flock_attraction"]/num_boids
			# Fly away from nearby boids
			if x_separation**2 + y_separation**2 < config["boids"]["avoidance_radius"]**2:
				xvs[i]-=x_separation
				yvs[i]-=y_separation
	# Try to match speed with nearby boids
	for i in range(num_boids):
		for j in range(num_boids):
			x_separation = (xs[j]-xs[i])
			y_separation = (ys[j]-ys[i])
			if x_separation**2 + y_separation**2 < config["boids"]["formation_flying_radius"]**2:
				xvs[i]+=(xvs[j]-xvs[i])*config["boids"]["speed_matching"]/num_boids
				yvs[i]+=(yvs[j]-yvs[i])*config["boids"]["speed_matching"]/num_boids

def move(xs,ys,xvs,yvs):
	# Move according to velocities
	num_boids = len(xs)
	for i in range(num_boids):
		xs[i]+=xvs[i]
		ys[i]+=yvs[i]