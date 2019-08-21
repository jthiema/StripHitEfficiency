# Check the runs infos from RunRegistry for Collisions in ExpressStream
# Output list saved in runlist.txt

import sys
from rhapi import RhApi, DEFAULT_URL

api = RhApi(DEFAULT_URL, debug = False)

#print api.folders()
#print api.tables('runreg_global')
#print api.tables('runreg_tracker')

def get_runs_in_fill(fill):
  q = "select r.runnumber, r.run_class_name, r.lhcfill, r.triggers, r.starttime, r.stoptime from runreg_tracker.runs r where r.run_class_name like :class and r.lhcfill = :fill order by r.runnumber asc"
  p = {"class": "Collisions%", "fill": str(fill) }
  qid = api.qid(q)
  #print api.query(qid)
  output = api.json(q, p)['data']
  
  runs={}  
  for run in output:
    runs[ int(run[0]) ] = {'CLASSNAME':run[1], 'FILL':run[2], 'TRIGGERS':run[3], 'STARTTIME':run[4], 'STOPTIME':run[5]}
  return runs

def get_run_certif(run):
  q = "select r.run_number, r.run_class_name, r.rda_name, r.rda_cmp_pixel, r.rda_cmp_strip, r.rda_cmp_tracking from runreg_tracker.datasets r where r.run_number = :run and r.rda_state = :state"
  p = {"run": str(run), "state": "COMPLETED"}
  qid = api.qid(q)
  #print api.query(qid)
  output = api.json(q, p)['data']
  
  runs={}
  for run in output:
    if 'Express' in run[2]:
      runs[ int(run[0]) ] = {'DATASET':run[2], 'PIX':run[3], 'STRIP':run[4], 'TRACK':run[5]}
  return runs


	
#-----------------------------
if len(sys.argv)<2:
  print "Syntax is: python2.6 query.py FILLNUMBER"
  exit()

fillnumber=str(sys.argv[1])

outfile = open('runlist.txt', 'w')
runsInFill = get_runs_in_fill(fillnumber)
for run in runsInFill:
  run_certif = get_run_certif(run)
  if run in run_certif:
    outfile.write(str(run)+' '+runsInFill[run]['CLASSNAME']+' '+run_certif[run]['DATASET']+' '+str(runsInFill[run]['FILL'])+' '+run_certif[run]['PIX']+' '+run_certif[run]['STRIP']+' '+run_certif[run]['TRACK']+' '+str(runsInFill[run]['TRIGGERS'])+'\n')
outfile.close()
