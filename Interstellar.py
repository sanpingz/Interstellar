#!/usr/bin/env python
"""
===== Merchant's Guide to the Galaxy =====
 \======================================/

TARS is a robot. These days he learned to 
convert intergalactic numerals and units.
Now show time!
------------------------------------------
"""

# Design:
# 
# class Converter is used to convert Roman numerals to a number.
# It provides two statc mathods, one is for converting, and another is used to verify the convert rules.
# 
# class Robot is designed as a paraent class, which only provide methods for putting and getting data.
# 
# class TARS is inherited from Robot. TARS provides learn and answer method. If the given statement is 
# not a question, TARS will parse and store the units related info into memory. If it is a question, TARS
# will parse the question and try to answer it based on the units info in memory.
# 
# The TARS works as a decorator. It will change the behavior of process function. Learn from a statement
# and try to answer a question.
# 
# 
# Usage:
# By default, find the input file named "input.txt" at current directory. Specify a input file by the first
# command line argument.

__author__ = 'sanpingz (zhangsp@163.com)'


import os
import re
import sys
from collections import Counter


class Converter:
	"""
	Converter is a kind of basic robot chip, which can convert Roman numerals to a number.
	"""

	# rate of exchange (ROE)
	ROE = dict(
		I = 1,
		V = 5,
		X = 10,
		L = 50,
		C = 100,
		D = 500,
		M = 1000
	)

	@staticmethod
	def convert_roman(symbols):
		"""
		Convert Roman numerals to number
		"""
		if not Converter.check_roman(symbols):
			return None
		numbers = [ Converter.ROE[s] for s in symbols ]
		for i in range(len(numbers)-1):
			if numbers[i] < numbers[i+1]:
				numbers[i] = -numbers[i]
		return sum(numbers)

	@staticmethod
	def check_roman(symbols):
		"""
		Verify the symbols succession are valid Roman numerals.
		"""
		# Rule 1: The symbols "I", "X", "C", and "M" can be repeated three times in succession, but no more.
		# (They may appear four times if the third and fourth are separated by a smaller value, such as XXXIX.)
		# "D", "L", and "V" can never be repeated.
		if not symbols and not isinstance(symbols, str):
			return False
		cnt = Counter(symbols)
		if cnt['I'] > 3:
			return False
		if cnt['X'] > 4 or (cnt['X'] == 4 and not re.match(r'\w*XXX[IV]X', symbols)):
			return False
		if cnt['C'] > 4 or (cnt['C'] == 4 and not re.match(r'\w*CCC[IVXL]C', symbols)):
			return False
		if cnt['M'] > 4 or (cnt['M'] == 4 and not re.match(r'\w*MMM[IVXLCD]M', symbols)):
			return False
		if cnt['D'] > 1 or cnt['L'] > 1 or cnt['V'] > 1:
			return False
		# Rule 2: "I" can be subtracted from "V" and "X" only. "X" can be subtracted from "L" and "C" only.
		# "C" can be subtracted from "D" and "M" only. "V", "L", and "D" can never be subtracted.
		# sequence = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
		for i in range(len(symbols)-1):
			if symbols[i] == 'I' and not symbols[i+1] in ['I', 'V', 'X']:
				return False
			elif symbols[i] == 'X' and not symbols[i+1] in ['I', 'V', 'X', 'L', 'C']:
				return False
			# 'C' can be at the left of any other symbols
			elif symbols[i] == 'V' and not symbols[i+1] in ['I']:
				return False
			elif symbols[i] == 'L' and not symbols[i+1] in ['I', 'V' ,'X']:
				return False
			elif symbols[i] == 'D' and not symbols[i+1] in ['I', 'V', 'X', 'L', 'C']:
				return False
		# Rule 3: Only one small-value symbol may be subtracted from any large-value symbol.
		# Checked in Rule 2	
		return True


class Robot:
	"""
	A basic robot only has a memory chip.
	"""

	memory = {}

	def put(self, key, subkey=None, value=None):
		if key and subkey and value:
			if key in self.memory:
				self.memory[key][subkey] = value
			else:
				self.memory[key] = { subkey: value }
		elif key and value:
			self.memory[key] = value

	def get(self, key, subkey=None):
		return self.memory.get(key) if not subkey else self.memory.get(key) and self.memory[key].get(subkey)


class TARS(Robot):
	"""
	TARS is robot, so he can put or get data from memory.

	"""

	default_answer = 'I have no idea what you are talking about'

	def __init__(self, func = None):
		self.func = func

	def __call__(self, msg):
		"""
		When TARS gets a message, he will try to understand it is a question or not.
		If it is not a question, TARS will learn from this message.
		Otherwise, TARS will try to answer this question based on his knowledge.
		"""
		if not self.is_question(msg):
			self.learn(msg)
		else:
			ans = self.answer(msg)
			if hasattr(self.func, '__call__'):
				self.func(ans)

	def is_question(self, msg):
		"""
		Simply predicate a question based on it starts with "how much/many" or not.
		"""
		return msg and re.match(r'how (?:much|many)', msg)

	def convert(self, symbols):
		"""
		Converter is a built-in chip in TARS, which can convert intergalactic numerals list to number.
		So TARS will convert intergalactic numerals to Roman numerals, and then convert it
		to number as the Credits.
		"""
		if not symbols or not isinstance(symbols, list):
			return None
		roman = [ self.get('NUMBERS', s) for s in symbols if self.get('NUMBERS') and s in self.get('NUMBERS') ]
		return None if len(symbols) != len(roman) else Converter.convert_roman(''.join(roman))

	def learn(self, msg):
		"""
		TARS will try to learn the intergalactic exchange rate and units.
		"""
		if not msg or not isinstance(msg, str):
			return
		words = msg.split()
		if re.match(r'\w+ is [IVXL]', msg):
			self.put('NUMBERS', words[0], words[-1])
		elif re.match(r'(?:\w+ )*\w+ is \d+ Credits', msg):
			symbols = re.findall(r'((?:\w+ )*)\w+ is \d+ Credits', msg)
			number = symbols and self.convert(symbols[0].split())
			if number:
				self.put('UNITS', words[-4], float(words[-2])/number)

	def answer(self, msg):
		"""
		TARS will try to answer this question based on the knowledge he learned before.
		"""
		if not msg or not isinstance(msg, str):
			return self.default_answer
		if re.match(r'how much', msg):
			symbols = re.findall(r'how much is ((?:\w+ )+)', msg)
			number = symbols and self.convert(symbols[0].split())
			if number:
				return '{0} is {1}'.format(' '.join(symbols), number)
		elif re.match('how many Credits', msg):
			symbols = re.findall(r'how many Credits is ((?:\w+ )+)\w+', msg)
			number = symbols and self.convert(symbols[0].split())
			matched_unit = re.findall(r'how many Credits is (?:(?:\w+ )+)(\w+)', msg)
			unit = matched_unit and matched_unit[0]
			if number and self.get('UNITS', unit):
				return '{0} {1} is {2:.0f} Credits'.format(' '.join(symbols), unit, number*self.get('UNITS', unit))
		return self.default_answer


@TARS
def process(msg):
	print(msg)


if __name__ == '__main__':
	INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
	if not os.path.isfile(INPUT_FILE):
		print("Can't find the input file: {file}".format(file=INPUT_FILE))
		exit(1)
	print(__doc__)
	with open(INPUT_FILE) as f:
		for line in f:
			process(line)