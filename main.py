from diffcalculator.internal import diffcalc


f1 = diffcalc.read_file("diffcalculator/tests/test_data/complex_file1.json")
f2 = diffcalc.read_file("diffcalculator/tests/test_data/complex_file2.json")
result = diffcalc.get_diff_v2(f1, f2)
print("\n".join(result))