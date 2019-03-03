filename = 'additional_xsudoku_rules.txt'

with open(filename, 'w') as f:

	for i in range(1, 10):
		for val in range(1, 10):
			curr_lit = 100 * i + 10 * i + val
			for j in range(1, 10):
				if i != j:
					other_lit = 100 * j + 10 * j + val
					f.write(str(-curr_lit) + ' ' + str(-other_lit) + ' 0\n')

	for i in range(1, 10):
		for val in range(1, 10):
			curr_lit = 100 * i + 10 * (10 - i) + val
			for j in range(1, 10):
				if i != j:
					other_lit = 100 * j + 10 * (10 - j) + val
					f.write(str(-curr_lit) + ' ' + str(-other_lit) + ' 0\n')
