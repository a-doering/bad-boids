import boids as bd
from matplotlib import pyplot as plt
from matplotlib import animation

config=bd.config
boids = bd.Boids(**config["boids"])
boids.initialize_boids()

figure=plt.figure()
axes=plt.axes(xlim=(config["plot"]["xlim"][0], config["plot"]["xlim"][1]), ylim=(config["plot"]["ylim"][0], config["plot"]["ylim"][1]))
scatter=axes.scatter(
   [b.position[0] for b in boids.boids], [b.position[1] for b in boids.boids]
   )

def animate(frame):
   boids.update_boids()
   scatter.set_offsets([b.position for b in boids.boids])

anim = animation.FuncAnimation(figure, animate,
                               frames=config["plot"]["frames"], interval=config["plot"]["interval"])

if __name__ == "__main__":
    plt.show()