#!/bin/bash

export OMPI_MCA_mpi_thread_multiple=0
export OMPI_MCA_opal_set_max_sys_limits=0
export OMPI_MCA_hwloc_base_binding_policy=none

DATE=$(date +%m%d)
NP=32

MPI_OPTS=(
  -np ${NP}
  --bind-to none
  -genv OMPI_MCA_mpi_thread_multiple 0
  -genv OMPI_MCA_hwloc_base_binding_policy none
)

SCRIPT_NAME="code_log"
SCRIPT_DIR=~/LG_WS2/${SCRIPT_NAME}
PIN_SCRIPT="${SCRIPT_DIR}/pin_socket.py"

# ── 各 Job 的個別設定 ─────────────────────────────────────────────────────────
# 格式："serial_number  ell  專案資料夾完整路徑"
declare -a JOBS=(
  "054 4 ~/LG_WS2/021_ell4_4545_257_w8_ml5_ie5075_job5_0624_log"
  # "042 3 ~/LG_WS2/020_ell3_4545_257_w8_ml5_ie5075_job4_0624_log"
)
PIDS=()
echo "=== Shell PID: $$ ==="

for i in "${!JOBS[@]}"; do
  read -r SERIAL_NUM ELL DIR_PATH <<< "${JOBS[$i]}"
  DIR_PATH=$(eval echo "${DIR_PATH}")   # 展開 ~ 字符
  JOB_NUM=$((i + 1))
  LOG_FILE="${SERIAL_NUM}_eval_chirality_job${JOB_NUM}_${DATE}.out"
  
  if [ ! -d "${DIR_PATH}" ]; then
    echo "[ERROR] Job ${JOB_NUM}: 找不到目錄 ${DIR_PATH}，跳過"
    continue
  fi
  
  echo "=== Job ${JOB_NUM} eval_chirality 開始: $(date) ==="
  (
    cd "${SCRIPT_DIR}" || { echo "[ERROR] 找不到 ${SCRIPT_DIR}"; exit 1; }
    export PIN_OFFSET=$(( i * NP ))     
    
    mpirun "${MPI_OPTS[@]}" \
      python -u "${PIN_SCRIPT}" \
      python -u eval_chirality.py \
      --l_charge "${ELL}" \
      --dir "${DIR_PATH}" \
      > "${LOG_FILE}" 2>&1
      
    echo "=== Job ${JOB_NUM} done: $(date) ==="
  ) &
  PIDS+=($!)
done

echo ""
echo "--- Waiting for all jobs to finish... ---"
ALL_OK=true
for i in "${!PIDS[@]}"; do
  PID=${PIDS[$i]}
  wait "${PID}"
  STATUS=$?
  JOB_NUM=$((i + 1))
  if [ ${STATUS} -eq 0 ]; then
    echo "  Job ${JOB_NUM} ✓  done"
  else
    echo "  Job ${JOB_NUM} ✗  FAILED (exit=${STATUS})"
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