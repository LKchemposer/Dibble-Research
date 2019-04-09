#!/usr/bin/env python3
import pandas as pd
import numpy as np
import sys

def species(df, ss):
    if ss == 'all':
        return df.columns[1:].values
    elif ss == 'cations':
        return df.columns[df.columns.str.contains('\+')].values
    elif ss == 'anions':
        return df.columns[df.columns.str.contains('-')].values
    elif type(ss) == list:
        return ss
    else: return df.columns[1:][~(df.columns[1:].str.contains('\+') |
                                  df.columns[1:].str.contains('-'))].values

def timestamps(df, ntimes):
    senses = [int(i.split('SENSIT')[1]) for i in df.keys() if 'SENSIT' in i]
    if ntimes == 'last':
        return [max(senses)]
    elif ntimes == 'all':
        return senses
    else: return senses[::int(ntimes)]

def clean_conc(df):
    df.columns = df.iloc[0, :].str.strip()
    df.drop(0, inplace=True)
    df = df.astype(float)
    return df

def clean_mod(df):
    df.drop([0, len(df) - 1], inplace=True)
    df.iloc[:, :3] = df.iloc[:, :3].astype(float)
    df.insert(0, 'k()', range(1, len(df) + 1))
    df = df.iloc[:, :5].shift()
    df.iloc[0, :] = ['k#', 'A', 'T^m', 'Ea', 'Reaction']
    return df

def clean_sens(df):
    t = float(df.iloc[0, 0].split()[-1])
    df.columns = df.iloc[1, :].str.strip()
    df.columns.name = ''
    df.drop('', axis=1, inplace=True)
    df.drop([0, 1], inplace=True)
    df = df.astype(float)
    df.reset_index(drop=True, inplace=True)
    return df, t

def analyze_nsa(path, specs='neutral', ntimes=5):
    assert type(path) == str, 'PATH should be a string'
    
    # loading spreadsheet
    print('Loading spreadsheet ...')
    ktc = pd.read_excel(path, sheet_name=None, header=None)
    conc, mod, spec = clean_conc(ktc['CONC']), clean_mod(ktc['model']), ktc['species']
    
    # species of interest
    ss = species(conc, specs)
    print('Species of interest:', ', '.join(ss))
    
    # dose rate = conc. of source?
    drate = spec[spec[0] == 'source'][2].values[0]
    print('Extracted dose rate: {} molecs/cc'.format(drate))
    
    # number of timestamps
    tstamps = timestamps(ktc, ntimes)
    
    # global G-values df
    Gs = pd.DataFrame(np.insert(ss, 0, 'Time')).transpose()

    with pd.ExcelWriter('output.xlsx') as w:
        mod.to_excel(w, sheet_name='model', header=False, index=False)
        print('Writing model to sheet')

        for i in tstamps:
            sheet = 'SENSIT{:03}'.format(i)

            # extract timestamp
            sens, t = clean_sens(ktc[sheet])
            print('Processing', sheet, '(at {:f} s)'.format(t))

            # G(t) = [X](t) / (dose rate * t)
            gs = conc.loc[(conc['Time(s)'] - t).abs().idxmin(), ss] / (drate * t)
            Gs = Gs.append(pd.DataFrame(np.insert(gs.values, 0, t)).transpose())

            try:
                # sort NSA by magnitude
                rcs = sens[ss].abs().apply(lambda i: i.sort_values(ascending=False).index)
            
            except KeyError:
                print(sheet, 'does not have some species of interest. Extracting available species ...')
                nss = [j for j in ss if j in sens.columns]
                if len(nss) == 0:
                    print(sheet, 'does not have any species of interest. Moving on ...')
                    continue
                rcs = sens[nss].abs().apply(lambda i: i.sort_values(ascending=False).index)
                
            rcs_s = 'k(' + (rcs + 1).astype(str) + ')'
            print('Sorting rate constants ...')

            # values per sorted index
            vals = rcs.apply(lambda i: sens.loc[:, i.name][i].values)
            nsa = rcs_s.append(vals).sort_index(kind='mergesort').reset_index(drop=True)
            nsa = nsa.shift()
            nsa.iloc[0, :] = nsa.columns

            # write to sheet for each timestamp
            nsa.to_excel(w, sheet_name='{:f}'.format(t), header=False, index=False)
            print('Writing to Excel ...')

        # write G-values df for all timestamps
        Gs.to_excel(w, sheet_name='G-values', header=False, index=False)
        print('Writing G-values to Excel ...')
    
    print('Analysis completed. Wrote to file "output.xlsx" in the current directory.')

with open(sys.argv[1], 'r') as ipt:
    lines = ipt.readlines()
    path, specs, ntimes = lines[0].strip(), lines[1].strip(), lines[2].strip().lower()
    if specs.split()[0].lower() == 'custom':
        specs = [i.upper() for i in specs.split()[1:]]
    analyze_nsa(path=path, specs=specs, ntimes=ntimes)