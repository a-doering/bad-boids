from matplotlib import pyplot as plt
from matplotlib import animation
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
	# Fly towards the middle
	for i in range(len(xs)):
		for j in range(len(xs)):
			x_separation = (xs[j]-xs[i])
			y_separation = (ys[j]-ys[i])
			xvs[i]+=x_separation*config["boids"]["flock_attraction"]/len(xs)
			yvs[i]+=y_separation*config["boids"]["flock_attraction"]/len(xs)
			# Fly away from nearby boids
			if x_separation**2 + y_separation**2 < config["boids"]["avoidance_radius"]**2:
				xvs[i]-=x_separation
				yvs[i]-=y_separation
	# Try to match speed with nearby boids
	for i in range(len(xs)):
		for j in range(len(xs)):
			x_separation = (xs[j]-xs[i])
			y_separation = (ys[j]-ys[i])
			if x_separation**2 + y_separation**2 < config["boids"]["formation_flying_radius"]**2:
				xvs[i]+=(xvs[j]-xvs[i])*config["boids"]["speed_matching"]/len(xs)
				yvs[i]+=(yvs[j]-yvs[i])*config["boids"]["speed_matching"]/len(xs)
	# Move according to velocities
	for i in range(len(xs)):
		xs[i]+=xvs[i]
		ys[i]+=yvs[i]

boids = init_boids()
figure=plt.figure()
axes=plt.axes(xlim=(config["plot"]["xlim"][0], config["plot"]["xlim"][1]), ylim=(config["plot"]["ylim"][0], config["plot"]["ylim"][1]))
scatter=axes.scatter(boids[0],boids[1])

def animate(frame):
   update_boids(boids)
   scatter.set_offsets(list(zip(boids[0],boids[1])))


anim = animation.FuncAnimation(figure, animate,
                               frames=config["plot"]["frames"], interval=config["plot"]["interval"])

if __name__ == "__main__":
    plt.show()
