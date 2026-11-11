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
PIN_SCRIPT=${SCRIPT_DIR}/pin_socket.py 

COMMON_ARGS=(
  --width  4.5
  --height 4.5
  --thick  0.257
  --w0     0.8
  --res    50
)
POL_TAG=lcp

# ── 各 Job 的個別設定 ─────────────────────────────────────────────────────────
# 格式："l_charge  serial_number  note  structure_npy完整路徑"
declare -a JOBS=(
  "2  053  optic  ~/LG_WS2/013_ell2_4545_257_w8_ml5_ie5075_job3_0602_log"
)

find_latest_struct() {
  local dir="${1/#\~/$HOME}/beta_data"
  local f name it best="" best_iter=-1
  if [ ! -d "$dir" ]; then echo "[ERROR] 找不到 $dir" >&2; return 1; fi
  for f in "$dir"/*structure_iter_*_beta_*.npy; do
    [ -f "$f" ] || continue
    name=$(basename "$f")
    it=$(echo "$name" | sed -E 's/.*structure_iter_([0-9]+)_beta_.*/\1/')
    it=$((10#$it))
    if [ "$it" -gt "$best_iter" ] || { [ "$it" -eq "$best_iter" ] && [[ "$name" != structure_* ]]; }; then
      best_iter=$it; best="$f"
    fi
  done
  if [ -z "$best" ]; then
    echo "[ERROR] $dir 內找不到 *structure_iter_*_beta_*.npy" >&2; return 1
  fi
  echo "$best"
}

PIDS=()
PID_JOB=()
PID_L=()

echo "=== Shell PID: $$ ==="
echo "=== POL_TAG: ${POL_TAG} ==="

for i in "${!JOBS[@]}"; do
  read -r L_CHARGE SERIAL_NUM NOTE PROJ_DIR <<< "${JOBS[$i]}"
  JOB_NUM=$((i + 1))
  NPY_PATH=$(find_latest_struct "${PROJ_DIR}") || { echo "[ERROR] Job ${JOB_NUM}: 找不到結構檔，跳過"; continue; }
  # 從檔名取 beta 與 iter（beta 會實際進入 mapping 的 tanh 投影，不只是標註）
  NPY_NAME=$(basename "${NPY_PATH}")
  BETA=$(echo "${NPY_NAME}" | sed -E 's/.*_beta_([0-9.]+)\.npy$/\1/')
  ITER=$(echo "${NPY_NAME}" | sed -E 's/.*structure_iter_([0-9]+)_beta_.*/\1/')
  LOG_FILE="${SERIAL_NUM}_ell${L_CHARGE}_fwd_${POL_TAG}_job${JOB_NUM}_${DATE}.out"
  TAG="${SERIAL_NUM}_ell${L_CHARGE}_fwd_${POL_TAG}_${DATE}_${NOTE}"
  echo "=== Job ${JOB_NUM} (l_charge=${L_CHARGE}, pol=${POL_TAG}) forward-only 開始: $(date) ==="
  echo "    結構: ${NPY_PATH}  (iter=${ITER}, beta=${BETA})"
  (
    cd ${SCRIPT_DIR} || { echo "[ERROR] 找不到 ${SCRIPT_DIR}"; exit 1; }
    mpirun "${MPI_OPTS[@]}" \
      python -u run_forward.py \
      "${COMMON_ARGS[@]}" \
      --l_charge  "${L_CHARGE}" \
      --tag       "${TAG}" \
      --struct    "${NPY_PATH}" \
      --beta      "${BETA}" \
      --pol       "${POL_TAG}" \
      --material_monitor 0.05 \
      > "${LOG_FILE}" 2>&1
    echo "=== Job ${JOB_NUM} done: $(date) ==="
  ) &
  PIDS+=($!); PID_JOB+=("${JOB_NUM}"); PID_L+=("${L_CHARGE}")
done

echo ""
echo "--- Waiting for all jobs to finish... ---"
ALL_OK=true
for k in "${!PIDS[@]}"; do
  wait "${PIDS[$k]}"
  STATUS=$?
  if [ ${STATUS} -eq 0 ]; then
    echo "  Job ${PID_JOB[$k]} (l_charge=${PID_L[$k]}, pol=${POL_TAG}) ✓  done"
  else
    echo "  Job ${PID_JOB[$k]} (l_charge=${PID_L[$k]}, pol=${POL_TAG}) ✗  FAILED (exit=${STATUS})"
    ALL_OK=false
  fi
done
echo ""
if ${ALL_OK}; then
  echo "=== All forward jobs finished successfully: $(date) ==="
else
  echo "=== Some jobs FAILED. Check .out log files. $(date) ==="
  exit 1
fi