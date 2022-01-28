import boids as bd
from nose.tools import assert_almost_equal, assert_equal
import os
import yaml


def test_config_loading():
    assert_equal(bd.config, yaml.safe_load(open("config.yaml")))

def test_bad_boids_regression():
    boids = bd.Boids(**bd.config["boids"])
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
