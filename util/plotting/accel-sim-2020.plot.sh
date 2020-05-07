
# GPGPU vs Accel Trace
./plot-correlation.py -H ../../run_hw/QUADRO-V100/ -c isca-v100-tracevsolde-perkernel.csv -r "GPGPU-Sim 3.x,Accel-Sim" -n -i pdf -b outliers.txt
cp ./correl-html/l2-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/l2-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
cp ./correl-html/l2-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/l2-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
cp ./correl-html/qv100_sm_cycles_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/qv100_sm_cycles_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
cp ./correl-html/dram-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/dram-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
cp ./correl-html/l2-read-hits_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/l2-read-hits_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
cp ./correl-html/warp-inst_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/warp-inst_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
cp ./correl-html/occupancy_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/occupancy_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
cp ./correl-html/l1readaccess_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/l1readaccess_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
cp ./correl-html/l1hitrate_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/l1hitrate_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
cp ./correl-html/ipc_QV100_old-EXEC_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/ipc_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf


pdfcrop ./ISCA20-Accelsim-Cameraready/figs/l2-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/l2-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/qv100_sm_cycles_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/dram-read-transactions_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/l2-read-hits_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/warp-inst_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/occupancy_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/l1readaccess_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/l1hitrate_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/ipc_QV100_old-EXEC_QV100_SASS-TRACE-per-app.pdf

# Trace versus Exec
./plot-correlation.py -H ../../run_hw/QUADRO-V100/ -c isca-v100-stracevsexec-perkernel.csv -r "Accel-Sim,Accel-Sim [PTX Mode]" -n -i pdf -m 1,2 -d ./cy.py -b outliers.txt
cp ./correl-html/qv100_sm_cycles_QV100_SASS-TRACE_QV100-EXEC.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/qv100_sm_cycles_QV100_SASS-TRACE_QV100-EXEC-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/qv100_sm_cycles_QV100_SASS-TRACE_QV100-EXEC-per-app.pdf

# GPGPU vs Accel-Trace Deep Bench
./plot-correlation.py -H ../../run_hw/QUADRO-V100 -c isca-v100-deepbench-all-perkernel.csv -r Accel-Sim -n -i pdf -d ./cy.py -m 1 -L 1.15 -b outliers.txt
cp ./correl-html/qv100_sm_cycles_QV100_SASS-TRACE.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/qv100_sm_cycles_QV100_SASS-TRACE-per-app.pdf
pdfcrop ./ISCA20-Accelsim-Cameraready/figs/qv100_sm_cycles_QV100_SASS-TRACE-per-app.pdf

# GPGPU versus Accel-Exec
#./plot-correlation.py -H ../../run_hw/QUADRO-V100/device-0/9.1/ -c isca-v100-newmodelvsold-perkernel.csv -r GPGPU-Sim,Accel-Sim-Trace -n -i png
#cp ./correl-html/l2-read-hits_QV100_old-EXEC_QV100-EXEC.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/
#cp ./correl-html/l2-read-hits_QV100_old-EXEC_QV100-EXEC.per-app.png ./ISCA20-Accelsim-Cameraready/figs/
#cp ./correl-html/l2-read-transactions_QV100_old-EXEC_QV100-EXEC.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/
#cp ./correl-html/l2-read-transactions_QV100_old-EXEC_QV100-EXEC.per-app.png ./ISCA20-Accelsim-Cameraready/figs/
#cp ./correl-html/l1readaccess_QV100_old-EXEC_QV100-EXEC.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/
#cp ./correl-html/l1readaccess_QV100_old-EXEC_QV100-EXEC.per-app.png ./ISCA20-Accelsim-Cameraready/figs/
#cp ./correl-html/l1hitrate_QV100_old-EXEC_QV100-EXEC.per-app.pdf ./ISCA20-Accelsim-Cameraready/figs/
#cp ./correl-html/l1hitrate_QV100_old-EXEC_QV100-EXEC.per-app.png ./ISCA20-Accelsim-Cameraready/figs/

# Turing exec
#./plot-correlation.py -H ../../run_hw/QUADRO-V100/device-0/9.1/ -c isca-turing-newmodel-perkernel.csv -r GPGPU-Sim,Accel-Sim-Exec -n -i png -b accel-sim-outliers.list | tee turing.txt
#./plot-correlation.py -H ~/github/tgrogers/gpgpu-sim_simulations/run_hw/TURING-RTX2060/10.1/ -r Accel-Sim-Exec -n -D RTX2060 -c ../../../../tgrogers/gpgpu-sim_simulations/util/plotting/isca-turing-newmodel-perkernel.csv -i pdf -b accel-sim-outliers.list | tee turing.txt
#./plot-correlation.py -H ~/github/tgrogers/gpgpu-sim_simulations/run_hw/TURING-RTX2060/10.1/ -r Accel-Sim-Trace -n -D RTX2060 -c ../../../../tgrogers/gpgpu-sim_simulations/util/plotting/isca-turing-trace-perkernel.csv -i pdf -b accel-sim-outliers.list | tee turing-volta-trace.txt
#./plot-correlation.py -H ~/github/tgrogers/gpgpu-sim_simulations/run_hw/TURING-RTX2060/10.1/ -r Accel-Sim-Trace,Accel-Sim-Exec -n -D RTX2060 -c ./isca-turing-execvstrace-perkernel.csv -i pdf -b accel-sim-outliers.list | tee turing-volta-trace.txt
#cp ./correl-html/l1hitrate_QV100_old-EXEC_QV100-EXEC.per-app.png ./ISCA20-Accelsim-Cameraready/figs/

# Pascal Trace
#./plot-correlation.py -H ../../run_hw/TITAN-X-PASCAL -c isca-titanx-newmodel-perkernel.csv -r GPGPU-Sim,Accel-Sim-Trace -n -i png -b accel-sim-outliers.list -v | tee pascal.txt
