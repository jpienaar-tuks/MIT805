#!/usr/bin/python3
import os, re, gzip, time

def F2C(f): #Fahrenheit 2 Celcius
    return (f-32)*5/9

def inch2mm(i): #inches 2 mm
    return i*25.4

def float_or_none(s, measure):
    r=re.match(r'[\.9 ]+',s)
    if r and r.end() == len(s):
        return ''
    else:
        if measure == 'T':
            return f'{F2C(float(s)):.1f}'
        elif measure == 'I':
            return f'{inch2mm(float(s)):.1f}'

start = time.time()
files={}
regex = re.compile(r'([A0-9]+-\d+)-\d+')
HEADER = 'STN, WBAN, YEAR, MONTH, DAY, MEAN_TEMP, MAX_TEMP, MIN_TEMP, PRCP\n'
line_data = "{stn}, {wban}, {year}, {month}, {day}, {mean_temp}, {max_temp}, {min_temp}, {prcp}\n"
all_files = sorted(os.listdir(os.path.join('..','gsod_all_years')))
file_count = len(all_files)

prev_stn_id=regex.match(all_files[0]).groups()[0]
for i, filename in enumerate(all_files):
    if i%1000==0:
        print(f'{i*100/file_count:.2f}%')        
    stn_id = regex.match(filename).groups()[0] #current
    if stn_id != prev_stn_id:
        files[prev_stn_id].close()
    if stn_id not in files:
        files[stn_id] = open(r'.\csv\{}.csv'.format(stn_id),'wt')
        files[stn_id].write(HEADER)
    with gzip.open(os.path.join('..','gsod_all_years',filename), 'rt') as f:
        f.readline()
        for line in f.readlines():
            stn, wban = stn_id.split('-')
            year = line[14:18]
            month = line[18:20]
            day = line[20:22]
            mean_temp = float_or_none(line[24:30],'T')
            max_temp = float_or_none(line[102:108],'T')
            min_temp = float_or_none(line[110:116],'T')
            prcp = float_or_none(line[118:123],'I')
            files[stn_id].write(line_data.format(**locals()))
    prev_stn_id = stn_id
print(f'That took {time.time()-start:.2f} s')
            
            
        
        
        
    
