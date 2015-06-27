#!/usr/bin/env python

import unittest
from Interstellar import TARS, Converter

class TestTARS (unittest.TestCase):

	def init_TARS(self):
		tars = TARS()
		with open('input.txt') as f:
			for line in f:
				not tars.is_question(line) and tars.learn(line)
		return tars

	def test_learn(self):
		input1 = 'glob is I'
		input2 = 'glob glob Silver is 34 Credits'
		tars = TARS()
		tars.learn(input1)
		self.assertEquals(tars.get('NUMBERS', 'glob'), 'I')
		tars.learn(input2)
		self.assertEquals(tars.get('UNITS', 'Silver'), 17)

	def test_answer(self):
		input1 = 'how much is pish tegj glob glob ?'
		input2 = 'how many Credits is glob prok Silver ?'
		input3 = 'how much wood could a woodchuck chuck if a woodchuck could chuck wood ?'
		tars = self.init_TARS()
		self.assertEquals(tars.answer(input1), 'pish tegj glob glob  is 42')
		self.assertEquals(tars.answer(input2), 'glob prok  Silver is 68 Credits')
		self.assertEquals(tars.answer(input3), 'I have no idea what you are talking about')

	def test_is_question(self):
		input1 = 'how much is pish tegj glob glob ?'
		input2 = 'how many Credits is glob prok Silver ?'
		input3 = 'pish pish Iron is 3910 Credits'
		tars = TARS()
		self.assertTrue(tars.is_question(input1))
		self.assertTrue(tars.is_question(input2))
		self.assertFalse(tars.is_question(input3))

	def test_convert(self):
		tars = self.init_TARS()
		self.assertEquals(tars.convert(['pish', 'tegj', 'glob', 'glob']), 42)


class TestConverter(unittest.TestCase):

	def test_convert_roman(self):
		self.assertEquals(Converter.convert_roman('MMVI'), 2006)
		self.assertEquals(Converter.convert_roman('MCMXLIV'), 1944)
		self.assertEquals(Converter.convert_roman('MCMIII'), 1903)


if __name__ == '__main__':
	unittest.main()


