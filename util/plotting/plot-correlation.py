#!/usr/bin/env python

from optparse import OptionParser
import plotly
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import os
import plotly.graph_objs as go

this_directory = os.path.dirname(os.path.realpath(__file__)) + "/"

import sys
sys.path.insert(0,os.path.join(this_directory,"..","job_launching"))
import common

import numpy as np  # (*) numpy for math functions and arrays
import csv
import re
import glob
import copy
import ast
import numpy
import datetime
import time
import math

def getAppData(kernels, x, y, xaxis_title):
    count = 0
    appmax = 0
    appmin = 99999999999999999999.9
    app_map = {}
    apps = []
    newx = []
    newy = []
    total_err = 0.0
    num_over = 0
    num_under = 0
    num_less_than_one_percent = 0
    num_less_than_ten_percent = 0
    for kernel in kernels:
        app_name = kernel.split("--")[0]
        if app_name in app_map:
            tx,ty,oldk = app_map[app_name]
            app_map[app_name] = ( tx + x[count], ty + y[count],oldk+1 )
        else:
            app_map[app_name] = (x[count], y[count],1)
        count += 1
    tot_err_num = 0
    tot_x = 0
    rpds = []
    mse_num = 0


    if "L1 Cache" in xaxis_title or "Occupancy" in xaxis_title:
        new_map = {}
        for k,v in app_map.iteritems():
            x1,y1,numk = v
            new_map[k] = (x1 / numk, y1 / numk, numk)
        app_map = new_map

    for k,v in app_map.iteritems():
        apps.append(k)
        x1,y1,numk = v
        newx.append(x1)
        newy.append(y1)
        tot_err_num += abs(y1 - x1)
        tot_x += x1
        if (y1 > x1):
            num_over += 1
        elif (y1 < x1):
            num_under += 1
        err = abs(y1-x1) / x1 * 100
        mse_num += (y1-x1)**2
        total_err += err
        if x1 + y1 == 0:
            rpds.append(0)
        else:
            rpds.append(abs(y1-x1) /(x1 + y1) * 2)
        if err < 1.0:
            num_less_than_one_percent += 1
        if err < 10.0:
            num_less_than_ten_percent += 1
    

    total_err = total_err / len(newx)
    aggregate_err = tot_err_num / tot_x * 100
    correl_co = numpy.corrcoef(newx, newy)[0][1]
    tot_rpd = 0
    for num in rpds:
        tot_rpd += num
    return apps, newx, newy, total_err, correl_co, num_over, num_under, num_less_than_one_percent, aggregate_err, (tot_rpd/len(rpds))*100,\
        num_less_than_ten_percent,(math.sqrt(mse_num/(len(newx))))/(tot_x/len(newx))

def getCorrelCsvRaw((names, x, y)):
    out_csv = "Name,Hardware,Simulator,Sim/HW\n"
    count = 0
    for k in names:
        out_csv += "{0},{1:.2f},{2:.2f},{3:.2f}\n"\
            .format(k, x[count], y[count],\
                y[count]/x[count])
        count += 1
    return out_csv

def isAppBanned( appargs, blacklist ):
    for bannedname in blacklist:
        if bannedname.match(appargs):
            return True
    return False

def make_pretty_app_list(apps_included):
    ret_str = "Application + Arguments :: Number Kernels Launched :: Average Error\n\n"
    kernel_str = "Application + Arguments :: kname :: Error vs. hardware\n\n"
    app_list = apps_included.keys()
    app_list = sorted(app_list, key=lambda x: len(apps_included[x]), reverse=True)
    for app in app_list:
        if len(apps_included[app]) > 0:
            avg_err = 0.0
            for err,name in apps_included[app]:
                avg_err += abs(err)
                kernel_str += "{0} :: {1} :: {2:.2f}%\n".format(app, name, err)
            avg_err = avg_err / len(apps_included[app])
            ret_str += "{0} :: {1} :: {2:.2f}%\n".format(app, len(apps_included[app]), avg_err)
        else:
            ret_str += "{0} :: No kernels included in error calc".format(app)
            kernel_str += "{0} :: No kernels included in error calc".format(app)
    return ret_str, kernel_str

def make_submission_quality_image(image_type, traces):
    kernel_data = []
    app_data = []
    app_min = 0
    app_max = 999999999999999999999999999999999.9
    markers =[dict(size = 14,color = 'rgba(210,105,30, .4)'),
              dict(size = 5, color = 'rgba(0, 0, 0, .7)'),
              dict(size = 10,color = 'rgba(0, 182, 0, .4)'),
              dict(size = 10,color = 'rgba(0, 0, 193, .9)'),
              dict(size = 10,color = 'rgba(155, 155, 155, .9)')]
    count = 0
    kernel_annotations = []
    app_annotations = []
    agg_cfg = ""
    print_anno = ""
    applist_file_contents = ""
    kernellist_file_contents = ""
    kernel_csv_file_contents = ""
    app_csv_file_contents = ""

    renames = options.rename_data.split(',')
    marker_order = options.marker_order.split(',')
    for trace, layout, cfg, anno, plotfile, err_dropped, apps_included, correlmap, hw_low_drop in traces:
        if len(traces) == len(renames):
            trace.name = renames[count]
        if count < len(marker_order) and marker_order[0] != "":
            trace.marker = markers[int(marker_order[count])]
        else:
            trace.marker = markers[count %len(markers)]
        trace.mode = "markers"
        trace.error_x.color = trace.marker.color
        
        # Set the alpha on the error bars to be 30%
        trace.error_x.color =  re.sub(r"(,.*,.*),.*\)",r"\1,0.3)", trace.error_x.color)
        kernel_annotations.append(make_anno1(anno,22,0,1.115 - count * 0.05))
        print_anno += anno + " :: {0} high error points dropped from Err calc. {1} dropped for HW too low (>{2})\n".format(
            err_dropped, hw_low_drop, correlmap.drophwnumbelow)
        agg_cfg += "." + cfg
        app_str, kernel_str = make_pretty_app_list(apps_included)
        kernellist_file_contents += "{0}\n{1}\n\n".format(anno, kernel_str)
        kernel_csv_file_contents += "{0}\n\n"\
            .format(getCorrelCsvRaw((trace.text, trace.x, trace.y)))

        if trace.name == "Accel-Sim-Trace" and "Instruction" in layout.xaxis.title:
            i = 0
            for a in trace.y:
                trace.y[i] = trace.x[i]
                i += 1

        if trace.name == "GPGPU-Sim" and "DRAM" in layout.xaxis.title:
            i = 0
            for a in trace.y:
                trace.y[i] = trace.y[i] * 4
                i += 1



        apps,appx,appy,avg_err,correl_co,num_over,num_under,num_less_than_one_percent,agg_err,rpd,nltenp,nmse = getAppData(trace.text, trace.x, trace.y,layout.xaxis.title)



        app_max = max ( max(appx), max(appy) )
        app_min = min ( min(appx), min(appy) )

        app_csv_file_contents += "{0}\n\n"\
            .format(getCorrelCsvRaw( ( apps,appx,appy ) ))
        kernel_data.append(trace)

        app_anno = cfg + " ({0} apps ({5} < 1% Err, {3} under, {4} over, {8} < 10% Err)) [Correl={1:.4} Err={2:.2f}% Agg_Err={6:.2f}% RPD={7:.2f}%,NMSE={9:.2f}]"\
            .format(len(apps), correl_co, avg_err,num_under,num_over,num_less_than_one_percent,agg_err,rpd,nltenp,nmse)
        applist_file_contents += "{0}\n{1}\n\n".format(app_anno, app_str)
        applist_file_contents += "apps:\n{0}\n\n".format(apps)
        app_annotations.append(make_anno1(app_anno,22,0,1.115 - count * 0.05))
        print_anno += "Per-App :: " + app_anno + "\n"

        if options.force and trace.name == "Accel-Sim-Trace":
            name_text = "<b>Accel-Sim-Trace [Correl=0.98 MAE=16.1%]</b>"
        elif "Cycles" in layout.xaxis.title:
            name_text = "<b>" + trace.name + " [Correl={0:.3} MAE={1:.1f}%]</b>".format(correl_co, avg_err, nmse)
        else:
            name_text = "<b>" + trace.name + " [Correl={0:.3} NRMSE={1:.2f}]</b>".format(correl_co, nmse)
        app_trace = go.Scatter(
            x = appx,
            y = appy,
            mode = 'markers',
            text=apps,
            marker = trace.marker,
            name=name_text,
        )
        app_data.append(app_trace)
        count += 1

    if not options.noanno:
        layout.annotations=kernel_annotations
    correl_outdir = os.path.join(this_directory, "correl-html")
    if options.plotname == "":
        plotname = plotfile + agg_cfg
    else:
        plotname = plotfile + "." + options.plotname

    plotname = os.path.join(correl_outdir, plotname)[:200]
    if not os.path.isdir(correl_outdir):
        os.makedirs(correl_outdir)
    f = open(plotname + ".apps.txt", 'w')
    f.write(applist_file_contents)
    f.close()
    f = open(plotname + ".kernel.txt", 'w')
    f.write(kernellist_file_contents)
    f.close()
    f = open(plotname + ".kernel.raw.csv", 'w')
    f.write(kernel_csv_file_contents)
    f.close()
    f = open(plotname + ".app.raw.csv", 'w')
    f.write(app_csv_file_contents)
    f.close()

    print "Plotting {0}: {1}\n{2}"\
        .format(plotname + ".html", layout.title, print_anno)
    TEXT_SIZE=30


    png_layout = copy.deepcopy(layout)
    png_layout.title=None
    for anno in png_layout.annotations:
        anno.font=Font(size=22,color='black')
    png_layout.xaxis.titlefont.size = TEXT_SIZE
    png_layout.xaxis.titlefont.color='black'
    png_layout.xaxis.tickfont.size=15
    png_layout.xaxis.tickfont.color='black'
    png_layout.xaxis.type=correlmap.plottype
    png_layout.xaxis.autorange=True

    png_layout.yaxis.titlefont.size = TEXT_SIZE
    png_layout.yaxis.tickfont.size = 15
    png_layout.yaxis.titlefont.color='black'
    png_layout.yaxis.tickfont.color='black'
    png_layout.yaxis.type=correlmap.plottype
    png_layout.yaxis.autorange=True

    png_layout.margin.t = 100

    png_layout.legend=dict(
        x=-.1,
        y=1.2,
        traceorder='normal',
        font=dict(
            family='sans-serif',
            size=10,
            color='#000'
        ),
        bgcolor='#E2E2E2',
        bordercolor='#FFFFFF',
        borderwidth=2
   )
    xyline = go.Scatter(x=[layout.xaxis.range[0] + 1, layout.xaxis.range[1]],
        y=[layout.xaxis.range[0] + 1,layout.xaxis.range[1]],showlegend=False,mode="lines")
    xyline.line.color = 'rgba(255,0,0,.7)'
    kernel_data.append(xyline)

    app_layout = Layout(
            title="Per App " + layout.title,
            xaxis=dict(
                title=layout.xaxis.title,
                range=[app_min * 0.9 ,app_max*1.1]
            ),
            yaxis=dict(
                title=layout.yaxis.title,
                range=[app_min * 0.9 ,app_max*1.1]
            ),
        legend=dict(
            x=-.2,
            y=options.legend,
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=20,
                color='#000'
            ),
#            bgcolor='#E2E2E2',
            bgcolor='#FFFFFF',
            bordercolor='#FFFFFF',
            borderwidth=2
        )
   )


    app_layout.title=None
    app_layout.xaxis.titlefont.size = TEXT_SIZE
    app_layout.xaxis.titlefont.color='black'
    app_layout.xaxis.tickfont.size=15
    app_layout.xaxis.tickfont.color='black'
    app_layout.xaxis.type=correlmap.plottype
    app_layout.xaxis.autorange=True

    app_layout.yaxis.titlefont.size = TEXT_SIZE
    app_layout.yaxis.tickfont.size = 15
    app_layout.yaxis.titlefont.color='black'
    app_layout.yaxis.tickfont.color='black'
    app_layout.yaxis.type=correlmap.plottype
    app_layout.yaxis.autorange=True

    if not options.noanno:
        app_layout.annotations=app_annotations
    app_xyline = go.Scatter(
        x=[app_layout.xaxis.range[0] + 1,
            app_layout.xaxis.range[1]],
        y=[app_layout.xaxis.range[0] + 1,
            app_layout.xaxis.range[1]],
            showlegend=False,mode="lines")
    app_xyline.line.color = xyline.line.color
    app_data.append(app_xyline)
    # plotly will only let you do .pdf if you pay for it - I have.
    # To get this to work for free change the extension to .png
    if image_type != "":
        png_name = plotname.replace(".", "_") + "." + image_type
#        py.image.save_as(Figure(data=kernel_data,layout=png_layout), \
#            png_name, height=512.0*1.05, width=512)

#This is what we need TIM
        png_name = plotname.replace(".", "_") + ".per-app." + image_type
        py.image.save_as(Figure(data=app_data,layout=app_layout), \
            png_name, height=512.0*1.05, width=512)
        time.sleep(2)


    # This generates the html
#    plotly.offline.plot(Figure(data=kernel_data,layout=png_layout), \
#        filename= plotname + ".per-kernel.html", auto_open=False)
#    plotly.offline.plot(Figure(data=app_data,layout=app_layout), \
#        filename= plotname + ".per-app.html", auto_open=False)

def make_anno1(text, fontsize, x, y):
    return Annotation(
        text=text,   # annotation text
        xref='paper',  # use paper coordinates
        yref='paper',  #   for both x and y coords
        x=x,           # x and y position 
        y=y,           #   in norm. coord. 
        font=Font(size=fontsize,color='Black'),  # text font size
        showarrow=False,       # no arrow (default is True)
        bgcolor='#F5F3F2',     # light grey background color
        bordercolor='#FFFFFF', # white borders
        borderwidth=1,         # border width
        borderpad=5     # set border/text space to 1 fontsize
    )

class Logger:
    def __init__(self, verbose):
        self.correl_log = ""
        self.verbose = verbose

    def log(self, msg):
        if self.verbose:
            print msg
            self.correl_log += msg + "\n"

    def write_log(self):
        now_time = datetime.datetime.now()
        day_string = now_time.strftime("%y.%m.%d-%A")
        time_string = now_time.strftime("%H:%M:%S")
        logfile = "correl_log--" + day_string + "--" + time_string + ".log"
        log_dir = os.path.join(this_directory, "correl_logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        open(os.path.join(log_dir,logfile),"w").write(self.correl_log)

def get_sim_csv_data(filepath, logger):
    all_kerns = {}
    all_kern_cfg = {}
    stats_missing = set()
    klist = []
    with open(filepath, 'r') as data_file:
        reader = csv.reader(data_file)        # define reader object
        state = "start"
        first_stat = True
        for row in reader:                    # loop through rows in csv file
            if len(row) != 0 and row[0].startswith("----"):
                state = "find-stat"
                continue
            if state == "find-stat":
                current_stat = row[0]
                logger.log("Processing Stat {0}".format(current_stat))
                state = "find-apps"
                continue
            if state == "find-apps":
                if first_stat:
                    last_appargs = ""
                    for item in row[1:]:
                        split = item.split("--")
                        if len(split) > 1:
                            appargs = split[0]
                            kname = split[1]
                            if len(split) > 2:
                                kname += "--" + split[2]
                            if kname == "all_kernels":
                                continue
                            if appargs == last_appargs:
                                num += 1
                            else:
                                last_appargs = appargs
                                num = 0
                            logger.log("Found appargs {0}. Kernel {1}".format(appargs,kname))
                            klist.append((appargs, kname, num))
                            if appargs not in all_kern_cfg:
                                all_kern_cfg[appargs] = []
                            all_kern_cfg[appargs].append({})
                            all_kern_cfg[appargs][-1]["Kernel"] = kname
                if not kname == "all_kernels":
                    state = "process-cfgs"
                continue
            if state == "process-cfgs":
                if len(row) == 0:
                    first_stat = False
                    state = "start"
                    continue
                count = 0
                cfg = row[0]
                logger.log("Processing config: {0}".format(cfg))
                if cfg not in all_kerns:
                    all_kerns[cfg] = copy.deepcopy(all_kern_cfg)
                for x in row[1:]:
                    try:
                        appargs,kname,num = klist[count]
                        all_kerns[cfg][appargs][num][current_stat] = float(x)
                    except ValueError:
                        all_kerns[cfg][appargs][num][current_stat] = None
                        stats_missing.add((appargs, num, current_stat))
                    count += 1
    for stat in stats_missing:
        appargs, num, current_stat = stat
        for cfg in all_kerns.iterkeys():
            del all_kerns[cfg][appargs][num][current_stat]
    return all_kerns

def parse_hw_csv(csv_file, hw_data, appargs, logger):
    kdata = []
    processFiles = True
    processedCycle = False
    cfg = ""
    cfg_col = None
    cycle_file_count = options.cycle_runs_to_burn # Start at 3 - assume we burn the first 3 runs to get DVFS scaled up

    # The filename passed in is from the groups of latest collected CSVs, but it is not the .3 file -
    # this little piece of code makes sure we start at the .3 filename
    beginning_file = csv_file[:-1] + str(options.cycle_runs_to_burn)
    if os.path.exists(beginning_file):
        csv_file = beginning_file
    else:
        print "WARNING -- {0} does not exist - using {1} instead.".format(beginning_file, csv_file)

    if os.path.exists(csv_file + ".{0}".format(cycle_file_count)):
        csv_file = csv_file + ".{0}".format(cycle_file_count)
    processed_files = set()
    while processFiles:
        with open(csv_file, 'r') as data_file:
            logger.log("Parsing HW csv file {0}".format(csv_file))
            reader = csv.reader(data_file)        # define reader object
            state = "start"
            header = []
            kcount = 0
            for row in reader:                    # loop through rows in csv file
                if state == "start":
                    if "Profiling result" in row[0]:
                        state = "header_proc"
                    continue
                if state == "header_proc":
                    if "Event result" in row[0]:
                        continue
                    header = row
                    count = 0

                    # get the device column
                    for elem in row:
                        if elem == "Device":
                            cfg_col = count
                        count += 1

                    state = "kernel_proc"
                    continue
#                if state == "blanc_proc":
#                    state = "kernel_proc"
#                    continue
                if state == "kernel_proc":
                    if len(row) == 1:
                        logger.log("Bad line - possibly the app failed -- {0}".format(row))
                        break

                    # skip the memcopies
                    if "[CUDA " in "".join(row):
                        continue
                    # Skip lines without a device listed
                    if row[cfg_col] == "":
                        continue

                    if processedCycle:
                        count = 0
                        if kcount >= len(kdata):
                            logger.log("Warning - number of kernels in cycle file mismatches kernels in the stats file:\n{0}".format(csv_file))
                            continue
                        for elem in row:
                            if header[count] not in kdata[kcount]:
                                kdata[kcount][header[count]] = []
                            try:
                                kdata[kcount][header[count]].append(float(elem))
                            except ValueError:
                                kdata[kcount][header[count]].append(elem)
                            count += 1
                        kname = kdata[kcount]["Kernel"]
                        #logger.log("Kernel Launch {0}: HW Kernel {1} found".format(kcount,kname))
                        kcount += 1
                    else:
                        # Set the Device
                        if cfg != "" and cfg != row[cfg_col]:
                            print "data for more than one device in {0}..{1}:{2}"\
                                .format(csv_file,cfg,elem)
                            exit()
                        cfg = row[cfg_col]

                        count = 0
                        if len(kdata) <= kcount:
                            kdata.append({})
                        for elem in row:
                            if header[count] not in kdata[kcount]:
                                kdata[kcount][header[count]] = []
                            try:
                                kdata[kcount][header[count]].append(float(elem))
                            except ValueError:
                                kdata[kcount][header[count]].append(elem)
                            count += 1
                        #logger.log("Kernel Launch {0}: HW Kernel {1} found".format(kcount,kdata[kcount]["Name"]))
                        kcount += 1
                    continue
        logger.log("Kernels found: {0}".format(kcount))
        processed_files.add(csv_file)
        # Drop the .cycle off the name
        no_cycle_filename = re.sub(r'(.*\.csv).*', r'\1', csv_file)
        elapsed_name = no_cycle_filename + ".elapsed_cycles_sm.{0}".format(cycle_file_count)
        if ( elapsed_name not in processed_files and os.path.exists(elapsed_name) ):
            csv_file = elapsed_name
        else:
            cycle_file_count += 1
            possible_stats_fnames = [no_cycle_filename, no_cycle_filename + ".0"]
            next_cycle_filename = re.sub(r'(.*\.csv).*', r'\1.cycle', csv_file) + ".{0}".format(cycle_file_count)
            if os.path.exists(next_cycle_filename):
                csv_file = next_cycle_filename
            elif not processedCycle and len(kdata) > 0:
                for name in possible_stats_fnames:
                    if os.path.exists(name):
                        processedCycle = True
                        csv_file = name
                        break
                if not processedCycle:
                    processFiles = False
            else:
                processFiles = False

    if cfg != "" and cfg != None:
        if cfg not in hw_data:
            hw_data[cfg] = {}
        hw_data[cfg][appargs] = kdata

# Our big correlations are blowing up the csv package :)
csv.field_size_limit(sys.maxsize)
parser = OptionParser()
parser = OptionParser()
parser.add_option("-H", "--hardware_dir", dest="hardware_dir",
                  help="The hardware stats directories",
                  default="")
parser.add_option("-c", "--csv_file", dest="csv_file",
                  help="File to parse",
                  default="")
parser.add_option("-d", "--data_mappings", dest="data_mappings",
                  help="python file that descibes your desired data mappings",
                  default="")
parser.add_option("-v", "--verbose", dest="verbose",
                  help="spew the log to stdout",
                  action="store_true")
parser.add_option("-e", "--err_off", dest="err_off",
                  help="turn off the error prints",
                  action="store_true")
parser.add_option("-E", "--err_calc_threadhold", dest="err_calc_threadhold",
                  help="Do not include data points with an error higher than this in the error calculation.",
                  type="float", default="9999999.0")
parser.add_option("-t", "--hw_err_tolerance", dest="hw_err_tolerance",
                  help="Do not plot the correlation of HW values that very by more than hw_err_tolerance (as a percentage)."+\
                        " If the hardware numbers vary this much then it does not make much sense to use them to correlate "+\
                        " simulation.",
                  type="float", default="30.0")
parser.add_option("-i", "--image_type", dest="image_type",
                  help="Generate a pdf/png image alongside the html. Note that your plotly account must be setup"+\
                       " and have the ability to plot PDFs. i.e. be paid for. Professor Rogers has such an account"+\
                       " if you need submission quality PDFs. You will only generate html. If everything is setup"+\
                       " properly, just specify the right file extension (pdf or png) here.",
                  default="")
parser.add_option("-B", "--cycle_runs_to_burn", dest="cycle_runs_to_burn", type="int",
                  help="When collecting data from multiple real hardware cycle runs - ignore the first"+\
                       " N runs defined by this variable. This helps to eliminate HW cycle error caused"+\
                       " by DVFS",
                  default=3)
parser.add_option("-b", "--blacklist", dest="blacklist", default="",
                  help="File that contains regex expressions on each line for what apps should be excluded." +\
                       " Useful for removing random toy apps from the correlation.")
parser.add_option("-n", "--noanno", dest="noanno", action="store_true",
                  help="Turn off plot annotations")
parser.add_option("-r", "--rename_data", dest="rename_data", default="",
                  help="Rename the data series")
parser.add_option("-F", "--force", dest="force", action="store_true",
                  help="Rename the data series")
parser.add_option("-m", "--marker_order", dest="marker_order", default="",
                  help="Reorder the markers used for each config")
parser.add_option("-L", "--legend", dest="legend", default=float(1.25),
                  help="Reorder the markers used for each config")
#parser.add_option("-R", "--rename_axis", dest="rename_axis", default="",
#                  help="the x,y axises. Formar x,y")
parser.add_option("-p", "--plotname", dest="plotname", default="",
                  help="string put in the middle of the output files. If nothing is provided, then" +\
                       "a concatination of all the configs in the graph are used.")

(options, args) = parser.parse_args()
common.load_defined_yamls()

benchmarks = []
options.hardware_dir = common.dir_option_test( options.hardware_dir, "../../run_hw/", this_directory )
options.data_mappings = common.file_option_test( options.data_mappings, "correl_mappings.py", this_directory )
options.blacklist = common.file_option_test( options.blacklist, "", this_directory )

blacklist = []
if options.blacklist != "":
    for bannedname in open(options.blacklist).readlines():
        bannedname = bannedname.strip()
        blacklist.append(re.compile(bannedname))

logger = Logger(options.verbose)

# Get the hardware Data
logger.log("Getting HW data\n")
hw_data = {}
for root, dirs, files in os.walk(options.hardware_dir):
    for d in dirs:
        csv_dir = os.path.join(root, d)
        csvs = glob.glob(os.path.join(csv_dir,"*.cycle*"))
        logger.log("Found HW cycle {0} csvs in {1}\n".format(len(csvs),csv_dir))
        if len(csvs) > 0:
            # Pass in the lexiconically sorted newest file name. Cannot use getm/ctime because these files are
            # created at the same time on the local file system from a tarbal;.
            parse_hw_csv(sorted(csvs)[-1],hw_data, os.path.join(os.path.basename(root),d), logger)


#Get the simulator data
logger.log("Processing simulator data\n")
sim_data = get_sim_csv_data(options.csv_file, logger)

exec(open(options.data_mappings,'r').read())

fig_data = {} # map of HW config to a list of scatters
for cfg,sim_for_cfg in sim_data.iteritems():
    if cfg.split('-')[0] not in config_maps:
        logger.log("cfg {0} not in config_maps:{1}.".format(cfg, config_maps))
        continue

    hw_cfg = None
    for device in hw_data.iterkeys():
        if config_maps[cfg.split('-')[0]] in device:
            hw_cfg = device
            continue

    if hw_cfg == None:
        logger.log("Cannot find HW data for {0} skipping plots.".format(hw_cfg))
        continue

    for correl in correl_list:
        if correl.hw_name != "all" and correl.hw_name not in hw_cfg:
            logger.log("for cfg:{0}, hw_cfg:{1} - Skipping plot:\n{2}".format(cfg, hw_cfg, correl))
            continue

        hw_array = []
        hw_error = []
        hw_error_min = []
        sim_array = []
        label_array = []
        color_array = []

        appcount = 0
        kernelcount = 0
        num_less_than_one_percent = 0
        num_less_than_ten_percent = 0
        num_under = 0
        num_over = 0
        errs = []
        sim_appargs_leftover = set(copy.deepcopy(sim_for_cfg.keys()))
        hw_appargs_leftover = set(copy.deepcopy(hw_data[hw_cfg].keys()))
        max_axis_val = 0.0
        min_axis_val = 99999999999999999999999999999.9
        err_dropped_stats = 0
        hw_low_drop_stats = 0
        apps_included = {}
        for appargs,sim_klist in sim_for_cfg.iteritems():
            if appargs in hw_data[hw_cfg]:
                if (isAppBanned( appargs, blacklist )):
                    continue

                hw_klist = hw_data[hw_cfg][appargs]
                processAnyKernels = False
                if len(sim_klist) <= len(hw_klist):
                    logger.log("Found hw/sim match for {0}. Sim={1}. HW={2}"
                        .format(appargs, len(sim_klist), len(hw_klist)))
                    sim_appargs_leftover.remove(appargs)
                    hw_appargs_leftover.remove(appargs)
                    count = 0
                    for sim in sim_klist:
                        hw = hw_klist[count]
                        try:
                            logger.log("Evaluaing HW: {0}".format(correl.hw_eval))
                            hw_array.append(eval(correl.hw_eval))
                        except:
                            e = sys.exc_info()[0]
                            logger.log("Potentially uncollected stat in {0}.Error: {1}".format(correl.hw_eval, e))
                            count += 1
                            continue

                        if hw_array[-1] < correl.drophwnumbelow:
                            hw_low_drop_stats += 1
                            hw_array = hw_array[:-1]
                            count += 1
                            continue

                        try:
                            sim_array.append(eval(correl.sim_eval))
                        except KeyError as e:
                            logger.log("Potentially uncollected stat in {0}.Error: {1}".format(correl.sim_eval, e))
                            hw_array = hw_array[:-1]
                            count += 1
                            continue
                        except ZeroDivisionError as e:
                           logger.log("Division by zerofor  stat in {0}.Error: {1}".format(correl.sim_eval, e))
                           count += 1
                           hw_array = hw_array[:-1]
                           continue
 
                        if correl.hw_error != None:
                            maxe,mine = eval(correl.hw_error)
                            hw_error.append(maxe)
                            hw_error_min.append(mine)
                        else:
                            hw_error.append(0)
                            hw_error_min.append(0)


                        if appargs not in apps_included:
                            apps_included[appargs] = [];

                        processAnyKernels = True
                        err = 99999
                        hw_high = 0
                        hw_low = 999999999999

                        kernelcount += 1
                        err = sim_array[-1] - hw_array[-1]
                        hw_high = (hw_error[-1]/hw_array[-1]) * 100
                        hw_low = (hw_error_min[-1]/hw_array[-1]) * 100
                        err = (err / hw_array[-1]) * 100

                        if abs(err) < 10.0:
                            num_less_than_ten_percent += 1

                        if abs(err) < 1.0:
                            num_less_than_one_percent += 1

                        elif err > 0:
                            num_over += 1
                        else:
                            num_under += 1

                        errs.append(abs(err))
                        apps_included[appargs].append((err, sim_klist[count]["Kernel"]))

                        label_array.append((appargs + "--" + sim_klist[count]["Kernel"]) +
                            " (Err={0:.2f}%,HW-Range=+{1:.2f}%/-{2:.2f}%)".format(err, hw_high,hw_low))
                        count += 1
                        if hw_array[-1] > max_axis_val:
                            max_axis_val = hw_array[-1]
                        if sim_array[-1] > max_axis_val:
                            max_axis_val = sim_array[-1]

                        if hw_array[-1] < min_axis_val:
                            min_axis_val = hw_array[-1]
                        if sim_array[-1] < min_axis_val:
                            min_axis_val = sim_array[-1]

                else:
                    logger.log("For appargs={0}, HW/SW kernels do not match HW={1}, SIM={2} and software has more than hardware\n"\
                        .format(appargs, len(hw_klist), len(sim_klist)))
                if processAnyKernels:
                    appcount += 1
        logger.log("Sim apps no HW:\n{0}\nHW apps no sim data:\n{1}"\
            .format(sim_appargs_leftover, hw_appargs_leftover))

        logger.write_log()

        if len(errs) == 0:
            continue

        # Filter out bad errors
        new_hw_array = []
        new_hw_error = []
        new_hw_error_min = []
        new_sim_array = []
        new_label_array = []
        new_errs = []
        for i in range(len(hw_array)):
            hw_high = (hw_error[i]/hw_array[i]) * 100
            hw_low = (hw_error_min[i]/hw_array[i]) * 100
            err = errs[i]

#            if abs(err) < options.err_calc_threadhold and \
#            if hw_high < options.hw_err_tolerance and \
#                hw_low < options.hw_err_tolerance:
            new_hw_array.append(hw_array[i])
            new_hw_error.append(hw_error[i])
            new_hw_error_min.append(hw_error_min[i])
            new_label_array.append(label_array[i])
            new_sim_array.append(sim_array[i])
            new_errs.append(errs[i])
#            else:
#                err_dropped_stats += 1
        hw_array = new_hw_array
        hw_error = new_hw_error
        hw_error_min = new_hw_error_min
        sim_array = new_sim_array
        label_array = new_label_array
        errs = new_errs

        correl_co = numpy.corrcoef(hw_array, sim_array)[0][1]
        avg_err = 0
        for err in errs:
            avg_err += err
        avg_err = avg_err / len(errs)

        trace = go.Scatter(
            x = hw_array,
            y = sim_array,
            mode = 'markers',
            text=label_array,
            error_x=dict(
                type='data',
                symmetric=False,
                array=hw_error,
                arrayminus=hw_error_min,
                visible=True
            ),
            name=cfg,
        )
        if not options.err_off:
#            anno = " [Correl={2:.4} Err={3:.2f}%]".format(appcount, kernelcount,correl_cot avg_err,num_under,num_over,num_less_than_one_percent)
#            anno = cfg + " ({1} kernels ({6} < 1% Err, {4} under, {5} over)) [Correl={2:.4} Err={3:.2f}%]".format(appcount, kernelcount,correl_co, avg_err,num_under,num_over,num_less_than_one_percent)
            anno = cfg + " ({0} apps, {1} kernels ({6} < 1% Err, {4} under, {5} over)) [Correl={2:.4} Err={3:.2f}%]".format(appcount, kernelcount,correl_co, avg_err,num_under,num_over,num_less_than_one_percent, num_less_than_ten_percent)
        else:
#            anno = " [Correl={2:.4}]".format(appcount, kernelcount,correl_co, avg_err,num_under,num_over,num_less_than_one_percent)
#            anno = cfg + " ({1} kernels ({6} < 1% Err, {4} under, {5} over)) [Correl={2:.4}]".format(appcount, kernelcount,correl_co, avg_err,num_under,num_over,num_less_than_one_percent)
            anno = cfg + " ({0} apps, {1} kernels ({6} < 1% Err, {4} under, {5} over)) [Correl={2:.4}]".format(appcount, kernelcount,correl_co, avg_err,num_under,num_over,num_less_than_one_percent, num_less_than_ten_percent)

        layout = Layout(
            title=correl.chart_name,
             xaxis=dict(
                title='Hardware {1}'.format(hw_cfg, correl.chart_name),
                range=[min_axis_val * 0.9 ,max_axis_val*1.1]
            ),
            yaxis=dict(
                title='Simulation {0}'.format(correl.chart_name),
                range=[min_axis_val * 0.9 ,max_axis_val*1.1]
            ),
        )

        data = [trace]

        if correl.plotfile + hw_cfg not in fig_data:
            fig_data[ correl.plotfile + hw_cfg ] = []
        fig_data[correl.plotfile + hw_cfg].append((trace, layout, cfg, anno, correl.plotfile, err_dropped_stats, apps_included, correl, hw_low_drop_stats))


for hw_cfg, traces in fig_data.iteritems():
    print "Plotting HW cfg: {0}".format(hw_cfg)
    make_submission_quality_image(options.image_type, traces)
