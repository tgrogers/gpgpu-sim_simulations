# This file is eval'd inside the plot-correlation.py file

# This maps the named GPGPU-Sim config to the card name reported in the nvprof file.
#   Every time you want to correlate a new configuration, you need to map it here.
config_maps = \
{
    "PUB_TITANX": "TITAN X (Pascal)",
    "TITANX_P102": "TITAN X (Pascal)",
    "TITANX": "TITAN X (Pascal)",
    "TITANX_OLD": "TITAN X (Pascal)",
    "TITANV": "TITAN V",
    "TITANV_OLD": "TITAN V",
    "3.x_PASCALTITANX" : "TITAN X (Pascal)",
    "3.x_P100" :  "Tesla P100",
    "P100_HBM" : "Tesla P100",
    "GTX480" : "GeForce GTX 480",
    "GTX1080Ti" : "GeForce GTX 1080 Ti",
    "QV100" : "Quadro GV100",
	"QV100_old" : "Quadro GV100",
	"QV100_SASS" : "Quadro GV100",
    "RTX2060" : "RTX2060",

}


# Every stat you want to correlate gets an entry here.
#   For cycles, the math is different for every card so we have differnt stats baed on the hardware.
import collections
CorrelStat = collections.namedtuple('CorrelStat', 'chart_name hw_eval hw_error sim_eval hw_name plotfile drophwnumbelow plottype')
correl_list = \
[
    # 1417 MHz
    CorrelStat(chart_name="Cycles",
        plotfile="titanv-cycles",
        hw_eval="np.average(hw[\"Duration\"])*1200",
        hw_error="np.max(hw[\"Duration\"])*1200 - np.average(hw[\"Duration\"])*1200,"+\
                 "np.average(hw[\"Duration\"])*1200 - np.min(hw[\"Duration\"])*1200",
        sim_eval="float(sim[\"gpu_tot_sim_cycle\s*=\s*(.*)\"])",
        hw_name="TITAN V",
        drophwnumbelow=8000,
		plottype="log"
    ),
    # 1417 MHz
    CorrelStat(chart_name="Cycles",
        plotfile="titanx-p102-cycles",
        hw_eval="np.average(hw[\"Duration\"])*1417",
        hw_error="np.max(hw[\"Duration\"])*1417 - np.average(hw[\"Duration\"])*1417,"+\
                 "np.average(hw[\"Duration\"])*1417 - np.min(hw[\"Duration\"])*1417",
        sim_eval="float(sim[\"gpu_tot_sim_cycle\s*=\s*(.*)\"])",
        hw_name="TITAN X (Pascal)",
        drophwnumbelow=8000,
        plottype="log"
    ),
    # (1400 MHz - 16-wide SIMD)
    CorrelStat(chart_name="Cycles",
        plotfile="gtx480-cycles",
        hw_eval="np.average(hw[\"Duration\"])*1400",
        hw_error="np.max(hw[\"Duration\"])*1400 - np.average(hw[\"Duration\"])*1400,"+\
                 "np.average(hw[\"Duration\"])*1400 - np.min(hw[\"Duration\"])*1400",
        sim_eval="float(sim[\"gpu_tot_sim_cycle\s*=\s*(.*)\"])*2",
        hw_name="GeForce GTX 480",
        drophwnumbelow=8000,
        plottype="log"
    ),
    # 1480 MHz
    CorrelStat(chart_name="Cycles",
        plotfile="p100-cycles",
        hw_eval="np.average(hw[\"Duration\"])*1480",
        hw_error="np.max(hw[\"Duration\"])*1480 - np.average(hw[\"Duration\"])*1480,"+\
                 "np.average(hw[\"Duration\"])*1480 - np.min(hw[\"Duration\"])*1480",
        sim_eval="float(sim[\"gpu_tot_sim_cycle\s*=\s*(.*)\"])",
        hw_name="Tesla P100",
        drophwnumbelow=8000,
        plottype="log"
    ),
    # 1480 MHz
    CorrelStat(chart_name="Cycles",
        plotfile="1080ti-cycles",
        hw_eval="np.average(hw[\"Duration\"])*1480",
        hw_error="np.max(hw[\"Duration\"])*1480 - np.average(hw[\"Duration\"])*1480,"+\
                 "np.average(hw[\"Duration\"])*1480 - np.min(hw[\"Duration\"])*1480",
        sim_eval="float(sim[\"gpu_tot_sim_cycle\s*=\s*(.*)\"])",
        hw_name="GeForce GTX 1080 Ti",
        drophwnumbelow=8000,
        plottype="log"
    ),
    # 1132 MHz
#    CorrelStat(chart_name="Cycles",
#        plotfile="gv100-cycles",
#        hw_eval="np.average(hw[\"Duration\"])*1132",
#        hw_error="np.max(hw[\"Duration\"])*1132 - np.average(hw[\"Duration\"])*1132,"+\
#                 "np.average(hw[\"Duration\"])*1132 - np.min(hw[\"Duration\"])*1132",
#        sim_eval="float(sim[\"gpu_tot_sim_cycle\s*=\s*(.*)\"])",
#        hw_name="Quadro GV100",
#        drophwnumbelow=0,
#        plottype="log"
#    ),
    CorrelStat(chart_name="Cycles",
        plotfile="qv100_sm_cycles",
        hw_eval="np.average(hw[\"elapsed_cycles_sm\"])/80",
        hw_error="np.max(hw[\"elapsed_cycles_sm\"])/80 - np.average(hw[\"elapsed_cycles_sm\"])/80,"+\
                 "np.average(hw[\"elapsed_cycles_sm\"])/80 - np.min(hw[\"elapsed_cycles_sm\"])/80",
        sim_eval="float(sim[\"gpu_tot_sim_cycle\s*=\s*(.*)\"])",
        hw_name="Quadro GV100",
        drophwnumbelow=0,
        plottype="log"
    ),
    CorrelStat(chart_name="RTX 2060 SM Cycles",
        plotfile="rtx2060_sm_cycles",
        hw_eval="np.average(hw[\"gpc__cycles_elapsed.avg\"])",
        hw_error="np.max(hw[\"gpc__cycles_elapsed.avg\"]) - np.average(hw[\"gpc__cycles_elapsed.avg\"]),"+\
                 "np.average(hw[\"gpc__cycles_elapsed.avg\"]) - np.min(hw[\"gpc__cycles_elapsed.avg\"])",
        sim_eval="float(sim[\"gpu_tot_sim_cycle\s*=\s*(.*)\"])",
        hw_name="RTX2060",
        drophwnumbelow=0,
        plottype="log",
    ),
    CorrelStat(chart_name="Cycles",
        plotfile="titanx_sm_cycles",
        hw_eval="np.average(hw[\"elapsed_cycles_sm\"])/60",
        hw_error="np.max(hw[\"elapsed_cycles_sm\"])/60 - np.average(hw[\"elapsed_cycles_sm\"])/60,"+\
                 "np.average(hw[\"elapsed_cycles_sm\"])/60 - np.min(hw[\"elapsed_cycles_sm\"])/60",
        sim_eval="float(sim[\"gpu_tot_sim_cycle\s*=\s*(.*)\"])",
        hw_name="TITAN X (Pascal)",
        drophwnumbelow=0,
        plottype="log"
    ),


    # Common, non-cycle stats
    CorrelStat(chart_name="Warp Instructions",
        plotfile="warp-inst",
        hw_eval="np.average(hw[\"inst_executed\"])",
        hw_error=None,
        sim_eval="float(sim[\"gpgpu_n_tot_w_icount\s*=\s*(.*)\"])",
        hw_name="all",
        drophwnumbelow=0,
        plottype="log"
    ),
    CorrelStat(chart_name="L2 read hits",
        plotfile="l2-read-hits",
        hw_eval="np.average(hw[\"l2_tex_read_transactions\"])*np.average(hw[\"l2_tex_read_hit_rate\"])/100",
        hw_error=None,
        sim_eval="float(sim[\"\s+L2_cache_stats_breakdown\[GLOBAL_ACC_R\]\[HIT\]\s*=\s*(.*)\"])",
        hw_name="all",
        drophwnumbelow=0,
        plottype="log"
    ),
    CorrelStat(chart_name="L2 reads",
        plotfile="l2-read-transactions",
        hw_eval="np.average(hw[\"l2_tex_read_transactions\"])",
        hw_error=None,
        sim_eval="float(sim[\"\s+L2_cache_stats_breakdown\[GLOBAL_ACC_R\]\[TOTAL_ACCESS\]\s*=\s*(.*)\"])",
        hw_name="all",
        drophwnumbelow=0,
        plottype="log"
    ),
	CorrelStat(chart_name="DRAM reads",
        plotfile="dram-read-transactions",
        hw_eval="np.average(hw[\"dram_read_transactions\"])",
        hw_error=None,
#        sim_eval="float(sim[\"Read\s*=\s*(.*)\"])+float(sim[\"L2_Alloc\s*=\s*(.*)\"])*24",
        sim_eval="float(sim[\"total dram reads\s*=\s*(.*)\"])",
        hw_name="all",
        drophwnumbelow=0,
        plottype="log"
    ),

    CorrelStat(chart_name="Occupancy",
        plotfile="occupancy",
        hw_eval="np.average(hw[\"achieved_occupancy\"])*100",
        hw_error=None,
        sim_eval="float(sim[\"gpu_occupancy\s*=\s*(.*)%\"])",
        hw_name="all",
        drophwnumbelow=0,
        plottype="linear"
    ),

    CorrelStat(chart_name="Post-Coaleser Reads",
        plotfile="l1readaccess",
        hw_eval="np.average(hw[\"gld_transactions\"])",
        hw_error=None,
        sim_eval="float(sim[\"\s+Total_core_cache_stats_breakdown\[GLOBAL_ACC_R\]\[TOTAL_ACCESS\]\s*=\s*(.*)\"])",
        hw_name="all",
        drophwnumbelow=0,
        plottype="log"
    ),

    CorrelStat(chart_name="L1 Cache Hit Rate",
        plotfile="l1hitrate",
        hw_eval="np.average(hw[\"tex_cache_hit_rate\"])",
        hw_error=None,
        sim_eval="float(sim[\"\s+Total_core_cache_stats_breakdown\[GLOBAL_ACC_R\]\[HIT\]\s*=\s*(.*)\"])" +\
                 "/(float(sim[\"\s+Total_core_cache_stats_breakdown\[GLOBAL_ACC_W\]\[TOTAL_ACCESS\]\s*=\s*(.*)\"])" +\
                 "+float(sim[\"\s+Total_core_cache_stats_breakdown\[GLOBAL_ACC_R\]\[TOTAL_ACCESS\]\s*=\s*(.*)\"]) + 1) * 100",
        hw_name="all",
        drophwnumbelow=-1,
        plottype="linear"
    ),

]
