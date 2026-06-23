#!/bin/bash
# =============================================================================
# run_chirality_scan_parallel.sh
# 同時對 4 個結構執行 chirality_scan.py（0~10 zR，各出 11 張圖）
#
# 用法：
#   chmod +x run_chirality_scan_parallel.sh
#   nohup ./run_chirality_scan_parallel.sh &
# =============================================================================

export OMPI_MCA_mpi_thread_multiple=0
export OMPI_MCA_opal_set_max_sys_limits=0
export OMPI_MCA_hwloc_base_binding_policy=none

MPI_OPTS=(
  -np 1
  --bind-to none
  -genv OMPI_MCA_mpi_thread_multiple 0
  -genv OMPI_MCA_hwloc_base_binding_policy none
)

# ── 共用參數 ──────────────────────────────────────────────────────────────────
CODE_DIR=~/LG_WS2/code_log
COMMON_ARGS=(
  --width  4.5
  --height 4.5
  --thick  0.257
  --w0     0.8
  --minimum_length 0.05
  --eta_i  0.50
  --eta_e  0.75
  --res    50
  --beta   512.0
)

# ── 各 Job 的個別設定 ─────────────────────────────────────────────────────────
# 格式： "l_charge  .npy完整路徑"
# out 自動放到 npy 上兩層的 job 資料夾內（job_dir/chirality_propagation/）
declare -a JOBS=(
  "0  ~/LG_WS2/011_ell0_4545_257_w8_ml5_ie5075_job1_0602_log/beta_data/structure_iter_282_beta_512.00.npy"
  "1  ~/LG_WS2/012_ell1_4545_257_w8_ml5_ie5075_job2_0602_log/beta_data/structure_iter_282_beta_512.00.npy"
  "2  ~/LG_WS2/013_ell2_4545_257_w8_ml5_ie5075_job3_0602_log/beta_data/structure_iter_282_beta_512.00.npy"
  "3  ~/LG_WS2/014_ell3_4545_257_w8_ml5_ie5075_job4_0602_log/beta_data/structure_iter_282_beta_512.00.npy"
  "5  ~/LG_WS2/015_ell5_4545_257_w8_ml5_ie5075_job1_0602_log/beta_data/structure_iter_282_beta_512.00.npy"
  "5  ~/LG_WS2/016_ell5_4545_257_w8_ml5_ie5075_job2_0602_purity/beta_data/structure_iter_282_beta_512.00.npy"
    )

PIDS=()

echo "=== Chirality Scan: ${#JOBS[@]} jobs (parallel) | $(date) ==="

for i in "${!JOBS[@]}"; do
  read -r L_CHARGE NPY_PATH <<< "${JOBS[$i]}"
  NPY_PATH=$(eval echo "${NPY_PATH}")   # 展開 ~
  JOB_NUM=$((i + 1))

  if [ ! -f "${NPY_PATH}" ]; then
    echo "[ERROR] Job ${JOB_NUM}: 找不到 ${NPY_PATH}，跳過"
    continue
  fi

  # beta_data/ 的上一層就是 job 資料夾
  JOB_DIR=$(dirname "$(dirname "${NPY_PATH}")")
  OUT_DIR="${JOB_DIR}/chirality_propagation"
  LOG_FILE="chirality_job${JOB_NUM}_ell${L_CHARGE}.out"

  echo "--- Launching Job ${JOB_NUM}  l_charge=${L_CHARGE}  -> ${LOG_FILE}"
  echo "    npy: ${NPY_PATH}"
  echo "    out: ${OUT_DIR}"

  (
    cd "${CODE_DIR}" || { echo "[ERROR] 找不到 ${CODE_DIR}"; exit 1; }
    mpirun "${MPI_OPTS[@]}" python -u chirality_scan.py \
      "${COMMON_ARGS[@]}"        \
      --l_charge  "${L_CHARGE}"  \
      --npy       "${NPY_PATH}"  \
      --out       "${OUT_DIR}"   \
      > "${LOG_FILE}" 2>&1
  ) &

  PIDS+=($!)
  echo "    PID=$!"
done

echo ""
echo "--- Waiting for all jobs to finish... ---"

ALL_OK=true
for i in "${!PIDS[@]}"; do
  PID=${PIDS[$i]}
  wait "${PID}"
  STATUS=$?
  JOB_NUM=$((i + 1))
  read -r L_CHARGE _ <<< "${JOBS[$i]}"
  if [ ${STATUS} -eq 0 ]; then
    echo "  Job ${JOB_NUM} (l_charge=${L_CHARGE}) ✓  done"
  else
    echo "  Job ${JOB_NUM} (l_charge=${L_CHARGE}) ✗  FAILED (exit=${STATUS})"
    ALL_OK=false
  fi
done

echo ""
if ${ALL_OK}; then
  echo "=== All jobs finished successfully: $(date) ==="
else
  echo "=== Some jobs FAILED. Check .out log files. $(date) ==="
  exit 1
fi