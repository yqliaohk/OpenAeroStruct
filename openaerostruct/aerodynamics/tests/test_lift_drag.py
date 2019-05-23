import unittest

import numpy as np

from openmdao.api import Problem
from openmdao.utils.assert_utils import assert_check_partials

from openaerostruct.aerodynamics.lift_drag import LiftDrag
from openaerostruct.utils.testing import run_test, get_default_surfaces


class Test(unittest.TestCase):

    def test(self):
        surfaces = get_default_surfaces()

        comp = LiftDrag(surface=surfaces[0])

        run_test(self, comp)


    def test_derivs_with_sideslip(self):
        surfaces = get_default_surfaces()

        # Use Tail since it is not symmetric.
        comp = LiftDrag(surface=surfaces[1])

        prob = Problem()
        prob.model.add_subsystem('comp', comp)
        prob.setup(force_alloc_complex=True)

        prob['comp.alpha'] = 3.0
        prob['comp.beta'] = 15.0
        prob['comp.sec_forces'] = 10.0 * np.random.random(prob['comp.sec_forces'].shape)

        prob.run_model()

        check = prob.check_partials(compact_print=True, method='cs', step=1e-40)

        assert_check_partials(check)

if __name__ == '__main__':
    unittest.main()
