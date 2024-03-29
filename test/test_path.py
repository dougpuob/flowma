import unittest
import sys
import os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)


from source.lib.path import osdp_path


class test_path(unittest.TestCase):

    def test_basename(self):
        path_obj = osdp_path()
        path_list = [
            'MyFile.txt',
            'C:\\MyFile.txt',
            '/MyFile.txt',
            '/home/dougpuob/MyFile.txt',
            'C:\\home\\dougpuob\\MyFile.txt',
            'C:/home/dougpuob/MyFile.txt'
            ]
        for path in path_list:
            self.assertEqual(path_obj.basename(path), 'MyFile.txt', "path={}".format(path))

    def test_normpath_abs(self):
        path_obj = osdp_path()
        self.assertEqual(path_obj.normpath('c:/Windows'), 'c:\\Windows')
        self.assertEqual(path_obj.normpath('c:/Windows/.'), 'c:\\Windows')
        self.assertEqual(path_obj.normpath('c:/A/B/C\D\E'), 'c:\\A\\B\\C\\D\\E')
        self.assertEqual(path_obj.normpath('c:/A/B/C\.\E'), 'c:\\A\\B\\C\\E')
        self.assertEqual(path_obj.normpath('c:/A/B/C\..\E'), 'c:\\A\\B\\E')
        self.assertEqual(path_obj.normpath('c:/A/B/C\..\..\..\E'), 'c:\\E')
        self.assertEqual(path_obj.normpath('c:/A/B/C\..\.\..\E'), 'c:\\A\\E')
        self.assertEqual(path_obj.normpath('c:/A/B/C\D\\E'), 'c:\\A\\B\\C\\D\\E')

    def test_normpath_windows_abs(self):
        path_obj = osdp_path()
        self.assertEqual(path_obj.normpath_windows('c:/Windows'), 'c:\\Windows')
        self.assertEqual(path_obj.normpath_windows('c:/Windows/.'), 'c:\\Windows')
        self.assertEqual(path_obj.normpath_windows('c:/A/B/C\D\E'), 'c:\\A\\B\\C\\D\\E')
        self.assertEqual(path_obj.normpath_windows('c:/A/B/C\.\E'), 'c:\\A\\B\\C\\E')
        self.assertEqual(path_obj.normpath_windows('c:/A/B/C\..\E'), 'c:\\A\\B\\E')
        self.assertEqual(path_obj.normpath_windows('c:/A/B/C\..\..\..\E'), 'c:\\E')
        self.assertEqual(path_obj.normpath_windows('c:/A/B/C\..\.\..\E'), 'c:\\A\\E')
        self.assertEqual(path_obj.normpath_windows('c:/A/B/C\D\\E'), 'c:\\A\\B\\C\\D\\E')

    def test_normpath_windows_rel(self):
        path_obj = osdp_path()
        self.assertEqual(path_obj.normpath_windows('A/B/C\D\\E'), 'A\\B\\C\\D\\E')
        self.assertEqual(path_obj.normpath_windows('A/B/C\D\\E\\.'), 'A\\B\\C\\D\\E')
        self.assertEqual(path_obj.normpath_windows('A/B/C/..\D\\E'), 'A\\B\\D\\E')
        self.assertEqual(path_obj.normpath_windows('A/B/C/./..\D\\E'), 'A\\B\\D\\E')
        self.assertEqual(path_obj.normpath_windows('A/B/C/../..\D\\E'), 'A\\D\\E')
        self.assertEqual(path_obj.normpath_windows('A/B/C/../..\D\\E'), 'A\\D\\E')
        self.assertEqual(path_obj.normpath_windows('A/B/C/../../..\D\\E'), 'D\\E')

    def test_normpath_rel(self):
        path_obj = osdp_path()
        self.assertEqual(path_obj.normpath('A/B/C\D\\E'), 'A/B/C/D/E')
        self.assertEqual(path_obj.normpath('A/B/C/D\\E\\.'), 'A/B/C/D/E')
        self.assertEqual(path_obj.normpath('A/B/C/..\D\\E'), 'A/B/D/E')
        self.assertEqual(path_obj.normpath('A/B/C/./..\D\\E'), 'A/B/D/E')
        self.assertEqual(path_obj.normpath('A/B/C/../..\D\\E'), 'A/D/E')
        self.assertEqual(path_obj.normpath('A/B/C/../..\D\\E'), 'A/D/E')
        self.assertEqual(path_obj.normpath('A/B/C/../../..\D\\E'), 'D/E')

    def test_normpath_windows_special_cases(self):
        path_obj = osdp_path()
        self.assertEqual(path_obj.normpath_windows('c:/A/B/..\..\..\..\E'), 'c:\\E')
        self.assertEqual(path_obj.normpath_windows('A/B/C/../../../..\D\\E'), 'D\\E')

    def test_is_abs(self):
        path_obj = osdp_path()
        self.assertEqual(path_obj.is_abs('c:/File.txt'), True)
        self.assertEqual(path_obj.is_abs('/home/File.txt'), True)

    def test_is_rel(self):
        path_obj = osdp_path()
        self.assertEqual(path_obj.is_rel('File.txt'), True)
        self.assertEqual(path_obj.is_rel('home/File.txt'), True)

    def test_explorer_dir(self):
        path_obj = osdp_path()
        found_list = path_obj.explore_dir('.')
        self.assertEqual(len(found_list) > 0, True)


if __name__ == '__main__':
    unittest.main()
