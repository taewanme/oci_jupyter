FROM ubuntu:18.04
MAINTAINER Taewan Kim <taewanme@gmail.com>

ENV ddd aaaassss

RUN apt-get update \
    && apt-get install -y python-setuptools openjdk-11-jdk python3.6 python3-pip ssh libaio1 alien jq wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

RUN pip3 install jupyterlab jupyter_contrib_nbextensions \
    && pip3 install ipython-sql cx_oracle sqlalchemy pandas numpy \
    && pip3 install cx_oracle matplotlib jupyter_nbextensions_configurator \
    && pip3 install scikit-learn mglearn bokeh Seaborn scipy NLTK \
    && pip3 install beautifulsoup4

RUN jupyter contrib nbextension install --user \
     && jupyter nbextension enable snippets_menu/main \
     && jupyter nbextension enable snippets/main \
     && jupyter nbextension enable toc2/main \
     && jupyter nbextension enable equation-numbering/main \
     && jupyter nbextension enable varInspector/main \
     && jupyter nbextension enable tree-filter/index \
     && jupyter nbextension enable ruler/main \
     && jupyter nbextension enable execute_time/ExecuteTime \
     && python3.6 -m ipykernel install --user --name ADW

ENV ORACLINET_URL https://download.oracle.com/otn_software/linux/instantclient/193000/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm
ENV SQLPLUS_URL https://download.oracle.com/otn_software/linux/instantclient/193000/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm
ENV CLI_VERSION 2.6.2

ENV kkk dddddddaaaaaa1111111111111

RUN wget ${ORACLINET_URL} && wget ${SQLPLUS_URL} \
    && alien -i ./oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm \
    && alien -i ./oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm \
    && rm -rf oracle-instantclient* \
    && echo '/usr/lib/oracle/19.3/client64/lib' > /etc/ld.so.conf.doracle-instantclient.conf \
    && ldconfig

ENV ORACLE_HOME /usr/lib/oracle/19.3/client64
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN wget -qO- -O oci-cli.zip "https://github.com/oracle/oci-cli/releases/download/v${CLI_VERSION}/oci-cli-${CLI_VERSION}.zip" \
    && jar -xvf ./oci-cli.zip ./ \
    && pip3 install ./oci-cli/oci_cli-*-py2.py3-none-any.whl \
    && rm -rf ./oci-cli \
    && rm -rf ./oci-cli.zip

### Config

ENV OCI_JUPYTER_WALLET_DIR /root/ipython/autonomous_db_wallets
ENV OCI_JUPYTER_KEY_FILE_DIR /root/ipython/key_files
ENV OCI_JUPYTER_CONFIG_DIR /root/ipython/config

ENV OCI_JUPYTER_BASE_DIR /root/.oci_jupyter

ENV TNS_ADMIN_DIR /root/tns
ENV TNS_ADMIN /root/tns

ENV DEFAULT_PRIVATE_KEY_FILE_NAME oci_api_key
ENV DEFAULT_PUBLIC_PERM_FILE_NAME oci_api_key_pubulic.pem

ENV OCICLI_CONFIG_DIR /root/.oci
ENV OCI_CLI_CONFIG_FILE /root/.oci/config



RUN mkdir -p ${OCI_JUPYTER_BASE_DIR} \
    && mkdir -p /root/temp \
    && mkdir -p /root/.jupyter \
    && mkdir -p /root/.ipython/profile_default/startup/

ENV ddd aaaassssdddd1111dddd1111

COPY ./src/static/sqlnet.ora ${OCI_JUPYTER_BASE_DIR}
COPY ./src/static/.gitignore /root
COPY ./src/shell/start-notebook.sh /usr/local/bin
COPY ./src/static/jupyter_notebook_config.json /root/.jupyter
COPY ./src/static/ocicli.json.template ${OCI_JUPYTER_BASE_DIR}
COPY ./src/static/adb_info.json.template ${OCI_JUPYTER_BASE_DIR}
COPY ./src/static/oci_region_id.json ${OCI_JUPYTER_BASE_DIR}
COPY ./src/shell/config_oci_cli.sh /usr/local/bin/
COPY ./src/shell/config_connection_of_adw.sh /usr/local/bin/
COPY ./src/py/jupyter_notebook_config.py /root/.jupyter
COPY ./src/py/magic.py /root/.ipython/profile_default/startup/
COPY ./src/py/ipython_config.py /root/.ipython/profile_default/
COPY ./src/javascript/snippet/custom.js /root/.jupyter/custom/custom.js



RUN chmod 755 /usr/local/bin/config_oci_cli.sh \
     && chmod 755 /usr/local/bin/config_connection_of_adw.sh \
     && chmod 755 /usr/local/bin/start-notebook.sh

EXPOSE 8888
VOLUME ["/root/ipython"]

ENV aaa aaaa

WORKDIR /root
ENTRYPOINT ["/bin/bash", "start-notebook.sh"]
