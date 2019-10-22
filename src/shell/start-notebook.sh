#!/bin/bash
#
set -e

#if [ ! -d $OCI_JUPYTER_WALLET_DIR ]; then
#  mkdir -p $OCI_JUPYTER_WALLET_DIR
#fi

#if [ ! -d $OCI_JUPYTER_KEY_FILE_DIR ]; then
#  mkdir -p $OCI_JUPYTER_KEY_FILE_DIR
#fi

if [ ! -d $OCI_JUPYTER_CONFIG_DIR ]; then
  mkdir -p $OCI_JUPYTER_CONFIG_DIR
fi

#if [ ! -f ${OCI_JUPYTER_CONFIG_DIR}/ocicli.json ]; then
#  cp ${OCI_JUPYTER_BASE_DIR}/ocicli.json.template ${OCI_JUPYTER_CONFIG_DIR}/ocicli.json
#fi

#if [ ! -f ${OCI_JUPYTER_CONFIG_DIR}/adb_info.json ]; then
#  cp ${OCI_JUPYTER_BASE_DIR}/adb_info.json.template ${OCI_JUPYTER_CONFIG_DIR}/adb_info.json
#fi

#if [ -f ${OCI_JUPYTER_BASE_DIR}/oci_region_id.json ]; then
#  rm -rf ${OCI_JUPYTER_BASE_DIR}/oci_region_id.json
#fi

#wget http://taewan.kim/data/oci_region_id.json -P ${OCI_JUPYTER_BASE_DIR}

jupyter notebook
