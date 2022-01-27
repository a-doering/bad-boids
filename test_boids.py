import boids
from nose.tools import assert_almost_equal, assert_equal
import os
import yaml

def test_bad_boids_regression():
    regression_data=yaml.safe_load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    boid_data=regression_data["before"]
    boids.update_boids(boid_data)
    for after,before in zip(regression_data["after"],boid_data):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.01)
	
def test_bad_boids_init():
    x,y,xv,yv = boids.init_boids()
    assert_equal(len(x), boids.config["boids"]["num"])
    #TODO