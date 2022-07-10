import unittest

import numpy as np
import pytest
from helpers import proto_test_case

from extremitypathfinder.helper_classes import AngleRepresentation, Vertex
from extremitypathfinder import helper_classes


helper_classes.origin = Vertex((-5., -5.))


class HelperClassesTest(unittest.TestCase):
    def test_angle_repr(self):
        with pytest.raises(ValueError):
            AngleRepresentation(np.array([0.0, 0.0]))

        #
        # def quadrant_test_fct(input):
        #     np_2D_coord_vector = np.array(input)
        #     return AngleRepresentation(np_2D_coord_vector).quadrant
        #
        # data = [
        #     ([1.0, 0.0], 0.0),
        #     ([0.0, 1.0], 0.0),
        #     ([-1.0, 0.0], 1.0),
        #     ([0.0, -1.0], 3.0),
        #
        #     ([2.0, 0.0], 0.0),
        #     ([0.0, 2.0], 0.0),
        #     ([-2.0, 0.0], 1.0),
        #     ([0.0, -2.0], 3.0),
        #
        #     ([1.0, 1.0], 0.0),
        #     ([-1.0, 1.0], 1.0),
        #     ([-1.0, -1.0], 2.0),
        #     ([1.0, -1.0], 3.0),
        #
        #     ([1.0, 0.00001], 0.0),
        #     ([0.00001, 1.0], 0.0),
        #     ([-1.0, 0.00001], 1.0),
        #     ([0.00001, -1.0], 3.0),
        #
        #     ([1.0, -0.00001], 3.0),
        #     ([-0.00001, 1.0], 1.0),
        #     ([-1.0, -0.00001], 2.0),
        #     ([-0.00001, -1.0], 2.0),
        # ]
        #
        # proto_test_case(data, quadrant_test_fct)

        # TODO test:
        # randomized
        # every quadrant contains angle measures from 0.0 to 1.0
        # angle %360!
        #     rep(p1) > rep(p2) <=> angle(p1) > angle(p2)
        #     rep(p1) = rep(p2) <=> angle(p1) = angle(p2)
        # repr value in [0.0 : 4.0]

        def value_test_fct(input):
            np_2D_coord_vector = np.array(input)
            return AngleRepresentation(np_2D_coord_vector).value

        data = [
            ([1.0, 0.0], 0.0),
            ([0.0, 1.0], 1.0),
            ([-1.0, 0.0], 2.0),
            ([0.0, -1.0], 3.0),
            ([2.0, 0.0], 0.0),
            ([0.0, 2.0], 1.0),
            ([-2.0, 0.0], 2.0),
            ([0.0, -2.0], 3.0),
        ]

        proto_test_case(data, value_test_fct)

    def test_vertex_translation(self):
        data = [
            ([1., 1.], [6., 6.]),
            ([0., 0.], [5., 5.]),
            ([-12., -3.], [-7., 2.]),
            ([-4., 5.], [1., 10.]),
            ([3., -2.], [8., 3.]),
        ]

        def translation_test_fct(input):
            return Vertex(input).get_coordinates_translated().tolist()

        proto_test_case(data, translation_test_fct)

    def test_vertex_angle_repr(self):
        data = [
            ([0., -5.], 0.),
            ([-5., 0.], 1.),
            ([-6., -5.], 2.),
            ([-5., -6.], 3.),
        ]

        def angle_repr_test_fct(input):
            return Vertex(input).get_angle_representation()

        proto_test_case(data, angle_repr_test_fct)

    def test_vertex_distance_to_origin(self):
        data = [
            ([0., 0.], np.sqrt(50)),
            ([-5., 0.], 5.),
            ([0., -5], 5.),
            ([-3., -2.], np.sqrt(13)),
            ([2., 5.], np.sqrt(149)),
        ]

        def dist_to_origin_test_fct(input):
            return Vertex(input).get_distance_to_origin()

        proto_test_case(data, dist_to_origin_test_fct)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(HelperClassesTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()
