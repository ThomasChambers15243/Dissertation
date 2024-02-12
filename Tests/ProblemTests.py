import unittest
import importlib
from Tests import MethodTestFile


class Test_Q1(unittest.TestCase):
    def test_outputType(self):
        importlib.reload(MethodTestFile)
        # Check ACSII inputs work
        self.assertEqual(type(MethodTestFile.Q1("a")), int)
        self.assertEqual(type(MethodTestFile.Q1("abcdefghijkmnopqrstuvwxyz")), int)
        self.assertEqual(type(MethodTestFile.Q1("1234567890")), int)
        self.assertEqual(type(MethodTestFile.Q1("¬!\"£$%^&*()_+))|<>,.?/:;'@[{]}''``#~")), int)

        # Check in false inputs
        with self.assertRaises(TypeError) as ex:
            MethodTestFile.Q1(100)
        self.assertEqual(ex.exception.__class__, TypeError)

        with self.assertRaises(TypeError) as ex:
            MethodTestFile.Q1(True)
        self.assertEqual(ex.exception.__class__, TypeError)

        with self.assertRaises(TypeError) as ex:
            MethodTestFile.Q1(100.00)
        self.assertEqual(ex.exception.__class__, TypeError)

        with self.assertRaises(TypeError) as ex:
            MethodTestFile.Q1([100,100])
        self.assertEqual(ex.exception.__class__, TypeError)


    def test_sum(self):
        importlib.reload(MethodTestFile)
        self.assertEqual(MethodTestFile.Q1("a"), 97)
        self.assertEqual(MethodTestFile.Q1(" "), 0)
        self.assertEqual(MethodTestFile.Q1("abcdefghijkmnopqrstuvwxyz"), 2739)
        self.assertEqual(MethodTestFile.Q1("1234567890"), 525)
        self.assertEqual(MethodTestFile.Q1("¬!\"£$%^&*()_+))|<>,.?/:;'@[{]}''``#~"), 2479)
        self.assertEqual(MethodTestFile.Q1("Python"),642)

        # Logic is better to be avoided, but its a simple .txt load
        with open("TestFiles/RomeoJuilet.txt") as file:
            stringOfPlay = ""
            for line in file:
                for char in file:
                    stringOfPlay += char
            self.assertEqual(MethodTestFile.Q1(stringOfPlay), 11443225)

class Test_Q2(unittest.TestCase):
    def test_sum(self):
        importlib.reload(MethodTestFile)
        floatList = [('4990', '1116'), ('3687', '2976'), ('1814', '4687'), ('2377', '3341'), ('436', '4656'), ('3444', '1901'), ('4233', '4029'), ('2966', '2973'), ('2784', '4711'), ('3393', '4069')]
        self.assertEqual(MethodTestFile.Q2(floatList), 30127.4459)
        floatList = [('3182', '4951'), ('3014', '2519'), ('4346', '1905'), ('3840', '4423'), ('4092', '1638'), ('4556', '413'), ('3915', '14'), ('624', '4556'), ('815', '258'), ('692', '4254')]
        self.assertEqual(MethodTestFile.Q2(floatList), 29079.235600000004)
        floatList = [('715', '60'), ('1504', '4301'), ('1129', '3608'), ('2840', '3545'), ('1274', '2745'), ('3909', '352'), ('1352', '1322'), ('3442', '1500'), ('2426', '4063'), ('2930', '871'), ('4135', '2283'), ('195', '4716'), ('3549', '1412'), ('4260', '2751'),
                ('2521', '1029'), ('4408', '4690'), ('1712', '2928'), ('3822', '459'), ('3644', '733'), ('2803', '1938'), ('2678', '4287'), ('4305', '2953'), ('281', '4596'), ('4209', '2419'), ('2571', '1161'), ('1971', '1999'), ('2744', '130'), ('383', '2111'),
                ('1137', '4912'), ('2503', '3669'), ('2648', '1465'), ('4339', '761'), ('2108', '2725'), ('4570', '392'), ('175', '4621'), ('1745', '1320'), ('4816', '2875'), ('2482', '497'), ('3850', '4992'), ('1063', '1741'), ('4459', '1086'), ('744', '1634'),
                ('348', '4411'), ('2296', '1154'), ('1206', '1074'), ('318', '4337'), ('2011', '767'), ('1707', '4532'), ('1146', '3680'), ('1587', '4696'), ('3858', '239'), ('1378', '4174'), ('1409', '992'), ('1046', '2744'), ('4269', '3006'), ('760', '4928'),
                ('862', '616'), ('4272', '1252'), ('4873', '4844'), ('393', '1287'), ('2517', '2173'), ('2898', '2264'), ('655', '2715'), ('4869', '4946'), ('2986', '1163'), ('2653', '2628'), ('3576', '555'), ('3384', '1363'), ('4731', '4805'), ('4249', '4322'),
                ('3297', '2546'), ('94', '1750'), ('3478', '1679'), ('109', '611'), ('712', '1890'), ('585', '2404'), ('4986', '4261'), ('4515', '1889'), ('2981', '4213'), ('1582', '3149'), ('1311', '4724'), ('3211', '758'), ('2047', '2420'), ('4423', '1338'),
                ('422', '3054'), ('3538', '3763'), ('3929', '1624'), ('2694', '2231'), ('2078', '1162'), ('1551', '4859'), ('2869', '835'), ('321', '2947'), ('963', '3789'), ('583', '3287'), ('232', '4722'), ('3672', '1930'), ('2118', '2534'), ('4300', '5087'),
                ('4688', '3892'), ('3032', '3517')]
        self.assertEqual(MethodTestFile.Q2(floatList), 244963.82360000012)

class Test_Q3(unittest.TestCase):
    def test_valid_brackets(self):
        importlib.reload(MethodTestFile)
        valid = ["()", "[]", "{}", "()[]{}", "{[()]}"]
        for i in valid:
            self.assertTrue(MethodTestFile.Q3(i))
    def test_invalid_brackets(self):
        importlib.reload(MethodTestFile)
        invalid = ["((","))","({","})","][","}{","({[","]})","({[)}]"]
        for i in invalid:
            self.assertFalse(MethodTestFile.Q3(i))

# Too much logic, should refactor but its messy. This is so much cleaner
# and is just generating
class Test_Q4(unittest.TestCase):
    class Node:
        def __init__(self, data=0):
            self.next = None
            self.data = data

    def CreateList(self, data: list[int]):
        root = self.Node(data[0])
        node = root
        for i in data[1:]:
            node.next = self.Node(i)
            node = node.next
        return root

    def isNodeSorted(self, node):
        lastMin = -1
        while node.next is not None:
            self.assertGreaterEqual(node.data, lastMin)
            lastMin = node.data
            node = node.next

    def test_AlreadySortedList(self):
        importlib.reload(MethodTestFile)
        node = MethodTestFile.Q4(self.CreateList(list(range(10000))))
        self.isNodeSorted(node)

    def test_Sort(self):
        importlib.reload(MethodTestFile)
        # Backwards Test
        self.isNodeSorted(MethodTestFile.Q4(self.CreateList(list(range(10, 0, -1)))))
        # Large Backwards
        self.isNodeSorted(MethodTestFile.Q4(self.createList(list(range(10000, 0, -1)))))
        # Unsorted
        self.isNodeSorted(MethodTestFile.Q4(self.createList([1, 3, 2, 4, 5, 7, 6, 8, 9, 10])))
        self.isNodeSorted(MethodTestFile.Q4(self.CreateList([31,765475,324,5435,654,234,7548768,23435,756,2342])))
        self.isNodeSorted(MethodTestFile.Q4(self.CreateList([96879,5785,567,3543,234,243,23,98,6])))

class Test_Q5(unittest.TestCase):
    def testNoDups(self):
        raise NotImplementedError



'''
def run_Q1_Tests():
    Q1_Suite = unittest.TestLoader().loadTestsFromTestCase(Test_Q1)
    return unittest.TextTestRunner().run(Q1_Suite)

def run_Q2_Tests():
    Q2_Suite = unittest.TestLoader().loadTestsFromTestCase(Test_Q2)
    return unittest.TextTestRunner().run(Q2_Suite)

def run_Q3_Tests():
    Q3_Suite = unittest.TestLoader().loadTestsFromTestCase(Test_Q3)
    return unittest.TextTestRunner().run(Q3_Suite)

def run_Q4_Tests():
    Q4_Suite = unittest.TestLoader().loadTestsFromTestCase(Test_Q4)
    return unittest.TextTestRunner().run(Q4_Suite)
'''

def run_Q5_tests():
    Q5_Suite = unittest.TestLoader().loadTestsFromTestCase(Test_Q5)
    return unittest.TextTestRunner().run(Q5_Suite)