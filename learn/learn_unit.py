import unittest
import xmlrunner


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('start test')

    @classmethod
    def tearDownClass(cls):
        print('over test')

    @staticmethod
    def alphabet_war(letters):
        levels = {
            'w': 4,
            'p': 3,
            'b': 2,
            's': 1,
            'm': -4,
            'q': -3,
            'd': -2,
            'z': -1,
        }
        res = 0
        for e in letters:
            res += levels.get(e, 0)
        if res == 0:
            return 'Let\'s fight again!'
        return 'Right side wins!' if res < 0 else 'Left side wins!'

    def test_1(self):
        self.assertEqual(self.alphabet_war("z"), "Right side wins!")

    def test_2(self):
        self.assertEqual(self.alphabet_war("zdqmwpbs"), "Let's fight again!")

    def test_3(self):
        self.assertEqual(self.alphabet_war("wq"), "Left side wins!")

    def test_4(self):
        self.assertEqual(self.alphabet_war("zzzzs"), "Right side wins!")

    def test_5(self):
        self.assertEqual(self.alphabet_war("wwwwww"), "Left side wins!")
