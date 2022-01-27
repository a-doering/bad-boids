import boids as boids_lib
from matplotlib import pyplot as plt
from matplotlib import animation

config=boids_lib.config
boids = boids_lib.init_boids()

figure=plt.figure()
axes=plt.axes(xlim=(config["plot"]["xlim"][0], config["plot"]["xlim"][1]), ylim=(config["plot"]["ylim"][0], config["plot"]["ylim"][1]))
scatter=axes.scatter(boids[0],boids[1])

def animate(frame):
   boids_lib.update_boids(boids)
   scatter.set_offsets(list(zip(boids[0],boids[1])))


anim = animation.FuncAnimation(figure, animate,
                               frames=config["plot"]["frames"], interval=config["plot"]["interval"])

if __name__ == "__main__":
    plt.show()