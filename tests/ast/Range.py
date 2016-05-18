import unittest
import os
import sys

dir = os.path.dirname(__file__)
path = os.path.join(dir, '../..')
sys.path.insert(0, path)

from koala.ast.Range import Range, find_associated_values

class Test_Excel(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_Range_getter(self):
        range = Range('A1:A3', [10, 20, 30])
        self.assertEqual(range.value, [10, 20, 30])

    def test_Range_setter(self):
        range = Range('A1:A3', [10, 20, 30])
        range.value = [33, 44, 55]
        self.assertEqual(range.values(), [33, 44, 55])

    def test_range_sizes(self):
        range = Range('D1:F2', [1, 2, 3, 4, 5, 6])

        self.assertEqual((range.nrows, range.ncols), (2, 3))

    def test_get(self):
        range1 = Range('D1:F2', [1, 2, 3, 4, 5, 6])

        self.assertEqual(range1.get(2, 2), 5)

    def test_get_row_0(self):
        range1 = Range('D1:F2', [1, 2, 3, 4, 5, 6])
        range2 = Range('D2:F2', [4, 5, 6])

        self.assertEqual(range1.get(2, 0), range2)

    def test_get_col_0(self):
        range1 = Range('D1:F2', [1, 2, 3, 4, 5, 6])
        range2 = Range('D1:D2', [1, 4])

        self.assertEqual(range1.get(0, 1), range2)

    def test_range_must_not_be_scalar(self):
        with self.assertRaises(ValueError):
            Range('A3', [1])

    def test_range_must_not_be_scalar_2(self):
        with self.assertRaises(ValueError):
            Range('A3:A3', [1])

    def test_get_values(self):
        range1 = Range('D4:D6', [1, 2, 3])
        range2 = Range('F4:F6', [1, 2, 3])

    	self.assertEqual(find_associated_values(('4', 'C'), range1, range2), (1, 1))

    def test_get_values_raises_error(self):
        range1 = Range('A1:A3', [1, 2, 3])
        range2 = Range('B1:B3', [1, 2, 3])

        with self.assertRaises(Exception):
            get_values('C5', range1, range2)

    # def test_is_associated(self):
    #     range1 = Range('A1:A3', [1, 2, 3])
    #     range2 = Range('B1:B3', [1, 2, 3])

    #     self.assertEqual(range1.is_associated(range2), 'v')

    # def test_is_associated_horizontal(self):
    #     range1 = Range('A1:C1', [1, 2, 3])
    #     range2 = Range('A2:C2', [1, 2, 3])

    #     self.assertEqual(range1.is_associated(range2), 'c')

    # def test_is_not_associated(self):
    #     range1 = Range('A1:A3', [1, 2, 3])
    #     range2 = Range('B2:B4', [1, 2, 3])

    #     self.assertEqual(range1.is_associated(range2), None)

    # ADD
    def test_add_array_one(self):
        range1 = Range('A1:A3', [1, 2, 3])
        range2 = Range('B1:B3', [1, 2, 3])

        self.assertEqual(Range.apply_one('add', range1, range2, ('1', 'C')), 2) # 1 + 1 = 2

    def test_add_array_one_constant(self):
        range = Range('A1:A3', [1, 2, 3])
        constant = 2

        self.assertEqual(Range.apply_one('add', range, constant, ('1', 'C')), 3) # 1 + 2 = 3

    def test_add_all(self):
        range1 = Range('A1:A3', [1, 10, 3])
        range2 = Range('B1:B3', [3, 3, 1])

        self.assertEqual(Range.apply_all('add', range1, range2, ('1', 'C')).values(), [4, 13, 4])

    # SUBSTRACT
    def test_substract_one(self):
        range1 = Range('A1:A3', [1, 10, 3])
        range2 = Range('B1:B3', [3, 3, 1])

        self.assertEqual(Range.apply_one('substract', range1, range2, ('2', 'C')), 7) # 10 - 3 = 7
    
    # MULTIPLY
    def test_multiply_one(self):
        range1 = Range('A1:A3', [1, 10, 3])
        range2 = Range('B1:B3', [3, 3, 1])

        self.assertEqual(Range.apply_one('multiply', range1, range2, ('2', 'C')), 30) # 10 * 3 = 30

    # DIVIDE
    def test_divide_one(self):
        range1 = Range('A1:A3', [1, 30, 3])
        range2 = Range('B1:B3', [3, 3, 1])

        self.assertEqual(Range.apply_one('divide', range1, range2, ('2', 'C')), 10) # 30 / 3 = 10

    # IS_EQUAL
    def test_is_equal_one(self):
        range1 = Range('A1:A3', [1, 30, 3])
        range2 = Range('B1:B3', [3, 3, 1])

        self.assertEqual(Range.apply_one('is_equal', range1, range2, ('2', 'C')), False) # 30 == 3 is False

    # IS_EQUAL
    def test_is_not_equal_one(self):
        range1 = Range('A1:A3', [1, 30, 3])
        range2 = Range('B1:B3', [3, 3, 1])

        self.assertEqual(Range.apply_one('is_not_equal', range1, range2, ('2', 'C')), True) # 30 != 3 is True

    # IS_STRICTLY_SUPERIOR
    def test_is_strictly_superior_one(self):
        range1 = Range('A1:A3', [1, 30, 3])
        range2 = Range('B1:B3', [3, 3, 1])

        self.assertEqual(Range.apply_one('is_strictly_superior', range1, range2, ('2', 'C')), True) # 30 > 3 is True

    # IS_STRICTLY_INFERIOR
    def test_is_strictly_inferior_one(self):
        range1 = Range('A1:A3', [1, 30, 3])
        range2 = Range('B1:B3', [3, 3, 1])

        self.assertEqual(Range.apply_one('is_strictly_inferior', range1, range2, ('2', 'C')), False) # 30 < 3 is False

    # IS_SUPERIOR_OR_EQUAL
    def test_is_superior_or_equal_one(self):
        range1 = Range('A1:A3', [1, 30, 3])
        range2 = Range('B1:B3', [3, 3, 3])

        self.assertEqual(Range.apply_one('is_superior_or_equal', range1, range2, ('3', 'C')), True) # 3 >= 3 is True

    # IS_INFERIOR_OR_EQUAL
    def test_is_inferior_or_equal_one(self):
        range1 = Range('A1:A3', [1, 30, 3])
        range2 = Range('B1:B3', [3, 3, 3])

        self.assertEqual(Range.apply_one('is_inferior_or_equal', range1, range2, ('1', 'C')), True) # 1 <= 3 is False


if __name__ == '__main__':
    unittest.main()