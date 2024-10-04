# utils/test_functions.py

import unittest
from utils.util_functions import load_csv, export_stl
from cadquery import Workplane

class TestUtilityFunctions(unittest.TestCase):
    
    def test_load_csv_valid(self):
        points = load_csv('models/python/vent/points.csv')
        self.assertIsInstance(points, list)
        self.assertGreater(len(points), 0)
        self.assertIsInstance(points[0], tuple)
        self.assertEqual(len(points[0]), 2)
    
    def test_load_csv_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            load_csv('non_existent.csv')
    
    def test_load_csv_malformed(self):
        # Assuming 'malformed.csv' exists with some invalid lines
        points = load_csv('models/python/vent/malformed.csv')
        # Check that only valid lines are loaded
        self.assertIsInstance(points, list)
        # Further assertions based on 'malformed.csv' content
    
    def test_export_stl(self):
        # Create a simple model
        model = Workplane("XY").box(1, 1, 1)
        try:
            export_stl(model, 'test_export.stl')
            # Verify that 'stl_files/test_export.stl' exists
            from pathlib import Path
            stl_path = Path('stl_files') / 'test_export.stl'
            self.assertTrue(stl_path.is_file())
        except Exception as e:
            self.fail(f"export_stl raised an exception {e}")

if __name__ == '__main__':
    unittest.main()
