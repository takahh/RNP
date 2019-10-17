
import matplotlib.pyplot as plt

file = '/Users/tkimura/Desktop/RNP/zdock/RMSDresults/rmsd3600_2.txt'

rmsd_list = []
with open(file) as f:
    for lines in f.readlines():
        try:
            rmsd = lines.split()[6].replace(';', '')
        except IndexError:
            print(lines)
        rmsd_list.append(float(rmsd))

plt.hist(rmsd_list, bins=40)
plt.show()