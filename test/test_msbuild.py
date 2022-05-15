import unittest
import sys
import os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)


from source.lib.define import os_helper, os_kind
from source.toolchain.msbuild import msbuild, msvc_information


class test_msbuild(unittest.TestCase):

    def test_basic(self):
        if os_helper().get_oskind().value == os_kind.windows.value:
            msbld: msbuild = msbuild()
            self.assertEqual(len(msbld.msvc_info_list) > 0, True)

            for msvc_info in msbld.msvc_info_list:
                msvc_info: msvc_information = msvc_info
                self.assertEqual(len(msvc_info.vcvars_files) > 0, True)
                self.assertEqual(len(msvc_info.vcvars_jsons) > 0, True)


if __name__ == '__main__':
    unittest.main()
