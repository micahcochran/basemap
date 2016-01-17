"""
Image unittests that run examples and compare the image output to test
images locate in unittest_images/.
"""

#
# TODO: It might be nice if generated PNG files could go into a
#    temporary directory (tempfile.mkdtemp().)  It would also be nice if
#    those images could be kept for diagnostics.
#

from __future__ import print_function

import os
import subprocess
import sys
try:
    import unittest
except ImportError:
    # for new features, fallback to unittest backport for Python 2.4 - 2.6
    import unittest2 as unittest

from matplotlib.testing.compare import compare_images


######  Optional Imports  ######
# adds names to optional_import set
optional_imports = set()

# not really needed at the moment, but I'm keeping it for future tests
try:
    from PIL import Image
    optional_imports.add('PIL')
except ImportError:
    pass


class TestImageComparisonsExamples(unittest.TestCase):
    """
    These tests are in in the example/ folder of basemap.
    """
    def helper_runner(self, test_name, **kwargs):
        """
        Helper function that runs the test and compares the images.
        
        test_name -- python file test_name
        cl_parameter -- command line parameters sent to test
        image_names -- required iterable of image names to compare
        requirements -- set of optional python modules required by the test
                        example: set(['PIL'])
        """
        cl_parameters = kwargs.get('cl_parameters', '')
        image_names = kwargs.get('image_names', [])
        requirements = kwargs.get('requirements', set())
        
        if not os.path.exists(test_name):
            raise OSError('Could not find test "{0}"'.format(test_name))
            
        if len(image_names) == 0:
            raise IOError('image_names is empty.')
            

        # check that all optional imports are met, or the SkipTest
        if not requirements.issubset(optional_imports):
            raise unittest.SkipTest('Skipping test, could not import "{0}" need for test'.format(requirements))
        
        returncode = subprocess.call([sys.executable, test_name, cl_parameters])
        if returncode != 0:
            raise RuntimeError('subprocess.call test "{0}" returned code {1}'.format(test_name, returncode))
          
        for image_name in image_names:
            results = compare_images('unittest_images/' + image_name, 
                                    image_name, 10)
        
            if results is not None:
                raise RuntimeError(results)
       
        
        
    ########  Actual Tests  ########
# this displays an image and code does not currently plot to a png file
#    def test_geos_demo_2(self):
        #self.helper_runner('geos_demo_2.py', image_names=['geos_demo.png'], requirements=set(['PIL']))

    def test_plotmap_oo(self):
        self.helper_runner('plotmap_oo.py', image_names=['plotmap.png'])

    def test_save_background(self):
        self.helper_runner('save_background.py', image_names=['figure1.png', 'figure2.png'])
        
    def test_simpletest_oo(self):
        self.helper_runner('simpletest_oo.py', image_names=['simpletest.png'])
        


if __name__ == '__main__':
    from unittest import main
    main()
