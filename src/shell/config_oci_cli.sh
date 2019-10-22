#!/bin/bash

rm -rf ${OCICLI_CONFIG_DIR}/oci_*

if [ -f ${OCI_JUPYTER_KEY_FILE_DIR}/${PRIVATE_KEY_FILE_NAME} ]; then
  cp ${OCI_JUPYTER_KEY_FILE_DIR}/${PRIVATE_KEY_FILE_NAME} ${OCICLI_CONFIG_DIR}/${DEFAULT_PRIVATE_KEY_FILE_NAME}
fi

if [ ! -f ${OCI_JUPYTER_KEY_FILE_DIR}/${PRIVATE_KEY_FILE_NAME} ]; then
  ssh-keygen -b 2048 -t rsa -f ${OCICLI_CONFIG_DIR}/${DEFAULT_PRIVATE_KEY_FILE_NAME}  -q -N ""
fi

openssl rsa -in ${OCICLI_CONFIG_DIR}/${DEFAULT_PRIVATE_KEY_FILE_NAME}  -pubout -out ${OCICLI_CONFIG_DIR}/${DEFAULT_PUBLIC_PERM_FILE_NAME}
openssl pkey -in ${OCICLI_CONFIG_DIR}/${DEFAULT_PUBLIC_PERM_FILE_NAME} -pubin -pubout -outform DER | openssl md5 -c > temp.log
original_str=$(cat ./temp.log)
rm ./temp.log
pattern='(stdin)= '
replace=''
FINGER_PRINT=${original_str//$pattern/$replace}

echo '[DEFAULT]' > $OCI_CLI_CONFIG_FILE
echo "user=${USER_OCID}" >> $OCI_CLI_CONFIG_FILE
echo "fingerprint=${FINGER_PRINT}" >> $OCI_CLI_CONFIG_FILE
echo "key_file=${OCICLI_CONFIG_DIR}/${PRIVATE_KEY_FILE_NAME}" >> $OCI_CLI_CONFIG_FILE
echo "tenancy=${TENANCY_OCID}" >> $OCI_CLI_CONFIG_FILE
echo "region=${REGION_ID}" >> $OCI_CLI_CONFIG_FILE
chmod 600 $OCI_CLI_CONFIG_FILE

echo ''
echo ''
echo '===================================================='
echo "Public PEM File: ${OCICLI_CONFIG_DIR}/${DEFAULT_PUBLIC_PERM_FILE_NAME}"
echo '===================================================='
echo ''
echo ''
cat ${OCICLI_CONFIG_DIR}/${DEFAULT_PUBLIC_PERM_FILE_NAME}
echo ''
echo '>> copy the public key and add to api key in user'
echo '>> Help: http://taewan.kim/projects/oci-database-jupyter/'
echo ''
echo '===================================================='
echo "fingerpritn: $FINGER_PRINT"
echo '===================================================='

if [ ! -f ${OCI_JUPYTER_KEY_FILE_DIR}/${PRIVATE_KEY_FILE_NAME} ]; then
  cp ${OCICLI_CONFIG_DIR}/${DEFAULT_PRIVATE_KEY_FILE_NAME} ${OCI_JUPYTER_KEY_FILE_DIR}/${PRIVATE_KEY_FILE_NAME}
  # copy 메시지 출력
fi
