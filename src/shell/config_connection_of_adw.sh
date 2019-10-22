#!/bin/bash

WALLET_FILE="${OCI_JUPYTER_WALLET_DIR}/${WALLET_FILE_NAME}"

if [ ! -f ${WALLET_FILE} ]; then
    echo "Wallet Zip File(${WALLET_FILE_NAME}) doesn't exist!!!!"
    echo "Please add the Wallet Zip file (${WALLET_FILE_NAME}) in 'wallet' directory of Jupyter Home"
    exit 0
fi

if [ -d $TNS_ADMIN_DIR ]; then
    rm -rf $TNS_ADMIN_DIR
fi

mkdir -p $TNS_ADMIN_DIR

current_dir=${pwd}

cd $TNS_ADMIN_DIR
jar xvf ${WALLET_FILE}
cp -f ${OCI_JUPYTER_BASE_DIR}/sqlnet.ora ${TNS_ADMIN_DIR}

cd $current_dir

echo ""
echo ""
echo "=========================================================="
echo "It is Completed the configuration for connection of Autonomous DB(${DATABASE_NAME})"
echo "=========================================================="