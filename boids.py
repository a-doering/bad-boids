import random
import yaml
random.seed(42)
config = yaml.safe_load(open("config.yaml"))

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