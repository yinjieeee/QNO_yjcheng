#!/bin/bash

export OMPI_MCA_mpi_thread_multiple=0
export OMPI_MCA_opal_set_max_sys_limits=0
export OMPI_MCA_hwloc_base_binding_policy=none

MPI_OPTS=(
  -np 32
  --bind-to none
  -genv OMPI_MCA_mpi_thread_multiple 0
  -genv OMPI_MCA_hwloc_base_binding_policy none
)

# 使用 () 建立子程序 (subshell) 以隔離 cd 指令 [1]
echo "=== run ... ==="
  
(
    echo "=== Job 1 $! started: $(date) ==="
    cd ~/LG_WS2/code_log || { echo "ERROR: dir not found"; exit 1; }
    mpirun "${MPI_OPTS[@]}" python -u run.py \
      --width 4.5 \
      --height 4.5 \
      --thick 0.257 \
      --w0 0.8 \
      --l_charge 0 \
      --minimum_length 0.05 \
      --eta_i 0.50 \
      --eta_e 0.75 \
      --serial_number 011 \
      --note "job1_0602_log" \
      > job1_0602.out 2>&1

    echo "=== Job 1 done: $(date) ==="
) &

(
    echo "=== Job 2 $! started: $(date) ==="
    cd ~/LG_WS2/code_log || { echo "ERROR: dir not found"; exit 1; }
    mpirun "${MPI_OPTS[@]}" python -u run.py \
      --width 4.5 \
      --height 4.5 \
      --thick 0.257 \
      --w0 0.8 \
      --l_charge 1 \
      --minimum_length 0.05 \
      --eta_i 0.50 \
      --eta_e 0.75 \
      --serial_number 012 \
      --note "job2_0602_log" \
      > job2_0602.out 2>&1

    echo "=== Job 2 done: $(date) ==="
) &

(
    echo "=== Job 3 $! started: $(date) ==="
    cd ~/LG_WS2/code_log || { echo "ERROR: dir not found"; exit 1; }
    mpirun "${MPI_OPTS[@]}" python -u run.py \
      --width 4.5 \
      --height 4.5 \
      --thick 0.257 \
      --w0 0.8 \
      --l_charge 2 \
      --minimum_length 0.05 \
      --eta_i 0.50 \
      --eta_e 0.75 \
      --serial_number 013 \
      --note "job3_0602_log" \
      > job3_0602.out 2>&1

    echo "=== Job 3 done: $(date) ==="
) &

(
    echo "=== Job 4 $! started: $(date) ==="
    cd ~/LG_WS2/code_log || { echo "ERROR: dir not found"; exit 1; }
    mpirun "${MPI_OPTS[@]}" python -u run.py \
      --width 4.5 \
      --height 4.5 \
      --thick 0.257 \
      --w0 0.8 \
      --l_charge 3 \
      --minimum_length 0.05 \
      --eta_i 0.50 \
      --eta_e 0.75 \
      --serial_number 014 \
      --note "job4_0602_log" \
      > job4_0602.out 2>&1

    echo "=== Job 4 done: $(date) ==="
) &

# 等待背景任務結束 [2]
wait
echo "=== All jobs finished: $(date) ==="