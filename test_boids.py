import boids as bd
from nose.tools import assert_almost_equal, assert_equal
import os
import yaml
config = yaml.safe_load(open("config.yaml"))


# def test_bad_boids_regression():
#     regression_data=yaml.safe_load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
#     boid_data=regression_data["before"]
#     boids.update_boids(boid_data)
#     for after,before in zip(regression_data["after"],boid_data):
#         for after_value,before_value in zip(after,before): 
#             assert_almost_equal(after_value,before_value,delta=0.01)


# TODO write test
# TODO: figure out, why I always get fucking tuples when unpacking the dict config["boids"]


def test_bad_boids_regression():
    boids = bd.Boids(**config["boids"])
    print(boids.formation_flying_radius)
    regression_data=yaml.safe_load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    boids.initialize_from_data(regression_data["before"])
    boids.update_boids()
    for index, boid in enumerate(boids.boids):
        assert_almost_equal(
            boid.position[0], regression_data["after"][0][index], delta=0.01
        )
        assert_almost_equal(
            boid.position[1], regression_data["after"][1][index], delta=0.01
        )
        assert_almost_equal(
            boid.velocity[0], regression_data["after"][2][index], delta=0.01
        )
        assert_almost_equal(
            boid.velocity[1], regression_data["after"][3][index], delta=0.01
        )   



# def test_bad_boids_init():
#     x,y,xv,yv = boids.init_boids()
#     assert_equal(len(x), boids.config["boids"]["num"])
#     #TODO