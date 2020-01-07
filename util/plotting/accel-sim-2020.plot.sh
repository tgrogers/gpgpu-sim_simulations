
# GPGPU vs Accel
#./plot-correlation.py -H ../../run_hw/QUADRO-V100/device-0/9.1/ -c qv100-OldEXec-vs-Trace.csv -r GPGPU-Sim,Accel-Sim-Trace -n -i pdf -b accel-sim-outliers.list
#./plot-correlation.py -H ../../run_hw/QUADRO-V100/device-0/9.1/ -c qv100-OldEXec-vs-Trace.csv -r GPGPU-Sim,Accel-Sim-Trace -n -i png -b accel-sim-outliers.list
cp ./correl-html/l2-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l2-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/qv100_sm_cycles_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/qv100_sm_cycles_QV100_old-EXEC_QV100_SASS-TRACE.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/dram-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/dram-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l2-read-hits_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l2-read-hits_QV100_old-EXEC_QV100_SASS-TRACE.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/warp-inst_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/warp-inst_QV100_old-EXEC_QV100_SASS-TRACE.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/occupancy_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/occupancy_QV100_old-EXEC_QV100_SASS-TRACE.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l1readaccess_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l1readaccess_QV100_old-EXEC_QV100_SASS-TRACE.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l1hitrate_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l1hitrate_QV100_old-EXEC_QV100_SASS-TRACE.per-app.png ./ISCA2020-Accel-sim/figs/


# GPGPU vs Accel
#./plot-correlation.py -H ../../run_hw/QUADRO-V100/device-0/9.1/ -c qv100-NewExec-Trace.csv -r Accel-Sim-Trace,Accel-Sim-Exec -n -i png -m 1,2 -F -d ./cm_cy_only.py
#cp ./correl-html/qv100_sm_cycles_QV100_SASS-TRACE_QV100-EXEC.per-app.pdf ./ISCA2020-Accel-sim/figs/
#cp ./correl-html/qv100_sm_cycles_QV100_SASS-TRACE_QV100-EXEC.per-app.png ./ISCA2020-Accel-sim/figs/

# GPGPU vs Accel
#./plot-correlation.py -H ../../run_hw/TESLA-V100/device-7/10.1/ -c isca-v100-deepbench-perkernel2.csv -r Accel-Sim-Trace -n -i png -b accel-sim-outliers.list -d ./db_cm_cy_only.py -m 1 -L 1.15 -v
#cp ./correl-html/qv100_sm_cycles_QV100_SASS-TRACE.per-app.pdf ./ISCA2020-Accel-sim/figs/
#cp ./correl-html/qv100_sm_cycles_QV100_SASS-TRACE.per-app.png ./ISCA2020-Accel-sim/figs/

#./plot-correlation.py -H ../../run_hw/QUADRO-V100/device-0/9.1/ -c isca-v100-newmodelvsold-perkernel.csv -r GPGPU-Sim,Accel-Sim-Trace -n -i png
cp ./correl-html/l2-read-hits_QV100_old-EXEC_QV100-EXEC.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l2-read-hits_QV100_old-EXEC_QV100-EXEC.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l2-read-transactions_QV100_old-EXEC_QV100-EXEC.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l2-read-transactions_QV100_old-EXEC_QV100-EXEC.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l1readaccess_QV100_old-EXEC_QV100-EXEC.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l1readaccess_QV100_old-EXEC_QV100-EXEC.per-app.png ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l1hitrate_QV100_old-EXEC_QV100-EXEC.per-app.pdf ./ISCA2020-Accel-sim/figs/
cp ./correl-html/l1hitrate_QV100_old-EXEC_QV100-EXEC.per-app.png ./ISCA2020-Accel-sim/figs/

#./plot-correlation.py -H ../../run_hw/QUADRO-V100/device-0/9.1/ -c isca-turing-newmodel-perkernel.csv -r GPGPU-Sim,Accel-Sim-Trace -n -i png -b accel-sim-outliers.list | tee turing.txt
./plot-correlation.py -H ../../run_hw/TITAN-X-PASCAL -c isca-titanx-newmodel-perkernel.csv -r GPGPU-Sim,Accel-Sim-Trace -n -i png -b accel-sim-outliers.list -v | tee pascal.txt
