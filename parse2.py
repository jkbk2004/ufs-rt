#https://www.vipinajayakumar.com/parsing-text-with-python/
#https://medium.com/codex/how-to-automatically-generate-data-structure-for-sankey-diagrams-6082e332139f
#https://www.geeksforgeeks.org/extract-numbers-from-a-text-file-and-add-them-using-python/

import pandas as pd
import re
import plotly.graph_objects as go

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
    
def check_app( app, next_line ):
    if next_line.find("-DMOVING_NEST=ON") > 0:
        app=app+"-MOVING_NEST"
    if next_line.find("-D32BIT=ON") > 0:
        app=app+"-32BIT"
    if next_line.find("-DDEBUG=ON") > 0:
        app=app+"-DEBUG"
    return app

def check_append( apps, app ):
    do_append=1
    for x in apps:
        if str(x) == str(app):
            do_append=0
    return do_append

def set_apps( file, patt_compile, patt_run ):
    apps = []
    
    while True:
        next_line = file.readline()
        if not next_line:
            break;
        else:
            head=next_line[0:3]
            if head=='COM':
                exe=1
            else:
                exe=0
            if head=='RUN':
                run=1
            else:
                run=0
        if exe and patt_compile.match(next_line):
            app = find_between( next_line, "-DAPP=", " " )
            app = check_app( app, next_line )
            do_append = check_append( apps, app )
            app_wk=app
            if do_append:
                apps.append(str(app))

    return apps

def set_rtcase( file, patt_compile, patt_run, apps ):

    pairs={}

    for x in apps:
        file.seek(0)
        runs=[]
        apps_=[]
        while True:
            next_line = file.readline()
            if not next_line:
                break;
            else:
                head=next_line[0:3]
                if head=='COM':
                    exe=1
                else:
                    exe=0
                if head=='RUN':
                    run=1
                else:
                    run=0
            app=""
            if exe and patt_compile.match(next_line):
                app = find_between( next_line, "-DAPP=", " " )
                app = check_app( app, next_line )
                do_append = check_append( apps_, app )
                if do_append:
                    app_wk=app
           
            if run and patt_run.match(next_line):
                rtcase=next_line.split()[2]
                do_append = check_append( runs, rtcase )
                if do_append and x == app_wk:
                    runs.append(rtcase)
    
        pairs[str(x)] = runs
    
    return pairs

def set_rtlog( file_conf, pairs ):
    
    for key, vals in pairs.items():
        for val in vals:
            rtcase=str(val)
            exe = 0
            file = open(file_conf+'/ufs-weather-model/tests/RegressionTests_hera.intel.log','r')
            while True:
                next_line = file.readline()
                if not next_line:
                    break;
                else:
                    head=next_line[0:13]
                    if head=='Checking test':
                        if rtcase in next_line:
                            exe=1
                    if exe :
                        if '  0: The tota' in next_line:
                            wallclock = float(next_line[60:])
                            exe=0
            file.close()
            exe = 0
            file = open(file_conf+"/job_card/"+rtcase+"/job_card",'r')
            while True:
                next_line = file.readline()
                if not next_line:
                    break;
                else:
                    head=next_line[0:5]
                    if head=='#jkim':
                        cores_ = find_between( next_line, "-n ", " ./fv3.exe" )
                        cores  = float(cores_)
            file.close()
            
            print (int(cores), int(wallclock), int(cores*wallclock), key, rtcase)
           
    return pairs

if __name__ == '__main__':
    patt_compile = re.compile("^COMPILE")
    patt_run     = re.compile("^RUN")

    file_conf='/home/jong/test-strategy/ufs-weather-model/tests/rt.conf'
    file = open(file_conf,'r')
    apps = set_apps(file, patt_compile, patt_run)
    file.close()
    
    file = open(file_conf,'r')
    pairs = set_rtcase(file, patt_compile, patt_run, apps)
    file.close()
    
    file_conf='/home/jong/test-strategy'
    pairs = set_rtlog(file_conf, pairs)
    
