#!/usr/bin/env python3
import sys

period = {1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'Bo', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg',
          13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V',
          24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se',
          35: 'Br', 36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh',
          46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba',
          57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy', 67: 'Ho',
          68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta', 74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt',
          79: 'Au', 80: 'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At', 86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac',
          90: 'Th', 91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu', 95: 'An', 96: 'Cm', 97: 'Bk', 98: 'Cf', 99: 'Es', 100: 'Fm',
          101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db', 106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt', 110: 'Ds',
          111: 'Rg', 112: 'Cn', 113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts', 118: 'Og'}

with open(sys.argv[1], 'r') as f:
    scan = [i.lower().strip() for i in f.readlines()]
    
print('Reading file ...')

stat_pts, std_ortns, ends, params = [], [], [], []
count = 0

_ = [stat_pts.append(i) if 'stationary point found' in j else
     std_ortns.append(i) if 'standard orientation' in j else
     ends.append(i) if '--------' in j else
     params.append(i) if 'initial parameters' in j else
     i for i, j in enumerate(scan)]

print('Found {} scan points successfully converged. Extracting each scan point ...'.format(len(stat_pts)))

id_scan_param = [i for i in ends if i > params[0]][1:3]
scan_param = [i.split()[2] for i in scan[id_scan_param[0]:id_scan_param[1]] if 'scan' in i][0]

with open('output.txt', 'w') as f:
    for stat_pt in stat_pts:
        last_pt = [i for i in std_ortns if i < stat_pt][-1]
        xyz = [i for i in ends if (i > last_pt) & (i < stat_pt)][1:3]

        id_opt_param = [i for i in ends if i > stat_pt][2:4]
        opt_param = [i.split()[3] for i in scan[id_opt_param[0]:id_opt_param[1]] if scan_param in i][0]

        xyz_ls = [i.split() for i in scan[xyz[0] + 1:xyz[1]]]
        count += 1

        intro = ['Scan point {} out of {}, {} = {}\n'.format(count, len(stat_pts), scan_param.upper(), opt_param)]
        lines = [' {}\t\t{:>9}\t{:>9}\t{:>9}\n'.format(period[int(i[1])], i[3], i[4], i[5]) for i in xyz_ls]
        for line in intro + lines:
            f.write(line)
        print('Extracted scan point {} out of {}. Searching next scan point ...'.format(count, len(stat_pts), scan_param.upper(), opt_param))

print('Extracted all {} scan points.'.format(len(stat_pts)))