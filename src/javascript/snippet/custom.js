require(["nbextensions/snippets_menu/main"], function (snippets_menu) {
  var ocicli = {
    'name': 'OCI Jupyter',
    'sub-menu': [
      {
        'name': 'Documentation',
        'external-link' : 'http://taewan.kim/'
      },
      {
        'name': 'Setup Jupyter',
        'snippet' : ['%setup_jupyter']
      },      
      '---',
      {
        'name': 'List Compartments',
        'snippet' : ['%list_compartments']
      },            
      '---',
      {
        'name': 'AutonomousDB',
        'sub-menu': [
          {
            'name': 'Autonomous DB 인스 조회',
            'snippet': [
              "%%list_adb",
              "compartment_id = <Compartment OCID>"
            ]
          },
          {
            'name': 'Autonomous DB 생성',
            'snippet': [
              "%%create_adb",
              "compartment_ocid = <Compartment OCID>",
              "cpu = 1",
              "storage = 1",
              "db_name = <database name>",
              "display_name = <display database name>",
              "workload = <DW|OLTP>",
              "password = <password>",
              "auto_scaling = <True|False>",
            ]
          },                     
          {
            'name': 'Autonomous DB 시작',
            'snippet': [
              "%%start_adb",
              "adb_ocid = <Autonomous DB OCID>"
            ]
          },
          {
            'name': 'Autonomous DB 정지',
            'snippet': [
              "%%stop_adb",
              "adb_ocid = <Autonomous DB OCID>"
            ]
          },
          {
            'name': 'Autonomous DB 삭제',
            'snippet': [
              "%%delete_adb",
              "adb_ocid = <Autonomous DB OCID>"
            ]
          },
          {
            'name': 'Scale-up/Scale-down',
            'snippet': [
              "%%change_adb",
              "adb_ocid = <Autonomou DB OCID>",
              "cpu = 1",
              "storage = 1"
            ]
          }
        ]//end of submenu for AutonomousDB
      },//end of AutonomousDB      
      {
        'name': 'Object Storage',
        'sub-menu': [
          {
            'name': 'Bucket 목록 조회',
            'snippet': [
              "%%sh",
              "##Object Storage의 버킷 목록 조회",
              "",
              "compartment_id='<Compartment OCID>'",
              "",
              "oci db autonomous-database list \\",
              "--compartment-id $compartment_id"
            ]
          },
          {
            'name': 'Bucket 생성',
            'snippet': [
              "%%sh",
              "##Object Storage의 버킷 생성",
              "",
              "compartment_id='<Compartment OCID>'",
              "bucket_name='<bucket name>'",
              "",
              "oci os bucket create \\",
              "--compartment-id $compartment_id \\",
              "--name $bucket_name"
            ]
          },
          {
            'name': 'Object 목록 조회',
            'snippet': [
              "%%sh",
              "##Object 목록 조회",
              "",
              "bucket_name='<bucket name>'",
              "",
              "oci os object list  \\",
              "--bucket-name $bucket_name"
            ]
          },
          {
            'name': 'Object 업로드',
            'snippet': [
              "%%sh",
              "##Object 업로드",
              "",
              "bucket_name='<bucket name>'",
              "file='<file name>'",
              "",
              "oci os object put \\",
              "--bucket-name $bucket_name --file $file"
            ]
          },
          {
            'name': 'Object 다운로드',
            'snippet': [
              "%%sh",
              "##Object 다운로드",
              "",
              "bucket_name='<bucket name>'",
              "file='<file name in local file system>'",
              "name='<object name>'",
              "",
              "oci os object get \\",
              "--bucket-name $bucket_name --file $file --name $name",
              "",
              "pwd",
              "ls -al $name"
            ]
          }
        ]//end of submenu for Object Storage
      }//end of Object Storage
    ] //end of submenu for oci-cli
  };
  var adw = {
    'name': 'AutonomousDB',
    'sub-menu': [
      {
        'name': 'Documentation',
        'external-link' : 'http://taewan.kim/'
      },
      {
        'name': 'Config DB Info',
        'snippet' : ['%%config_db_info',
          'adb_id = <adb ocid>',
          'user = <uaer id: admin>',
          'password = <password: Welcome123456>',
          'profie = low|medium|high'
        ]
      },
      {
        'name': 'Use Database',
        'snippet' : ['%%use_adb',
          'adb_ocid = <ADB OCID>'
        ]
      },
      {
        'name': 'DB Connection',
        'snippet' : ['%connect_db']
      },
       '---',
       {
         'name': 'Loading Datasets',
         'sub-menu': [
           {
             'name': 'Boston House Price',
             'snippet' : [
               "from sqlalchemy import create_engine",
               "import pandas as pd",
               "from sklearn.datasets import load_boston",
               "import numpy as np",
               "",
               "boston = load_boston()",
               "features=np.append(boston.feature_names,np.array(['medv']))",
               "df = pd.DataFrame(np.c_[boston['data'], boston['target']], columns=features)",
               "",
               "conn_str=os.environ['PY_CONNECTION_STR']",
               "engine = create_engine(conn_str)",
               "",
               "df.to_sql('bostonhousing', engine, index=False, if_exists='replace')"
             ]
           },
           {
             'name': 'Boston Dataset 조회',
             'snippet' : [
               "%%sql",
               "",
               "select * from bostonhousing",
               "FETCH FIRST 20 ROWS ONLY"
             ]
           },
           "---",
           {
             'name': 'Iris Dataset',
             'snippet' : [
               "from sqlalchemy import create_engine",
               "import pandas as pd",
               "from sklearn.datasets import load_iris",
               "import numpy as np",
               "",
               "iris = load_iris()",
               "features=np.append(iris.feature_names,np.array(['target']))",
               "df = pd.DataFrame(data = np.c_[iris['data'],iris['target']], columns=features)",
               "",
               "conn_str=os.environ['PY_CONNECTION_STR']",
               "engine = create_engine(conn_str)",
               "",
               "df.to_sql('iris', engine, index=False, if_exists='replace')"
             ]
           },
           {
             'name': 'Iris Dataset 조회',
             'snippet' : [
               "%%sql",
               "",
               "select * from iris",
               "FETCH FIRST 20 ROWS ONLY"
             ]
           },
           "---",
           {
             'name': 'Breast Cancer',
             'snippet' : [
               "from sqlalchemy import create_engine",
               "import pandas as pd",
               "from sklearn.datasets import load_breast_cancer",
               "import numpy as np",
               "",
               "cancer = load_breast_cancer()",
               "features=np.append(cancer.feature_names,np.array(['target']))",
               "df = pd.DataFrame(data = np.c_[cancer['data'],cancer['target']], columns=features)",
               "",
               "conn_str=os.environ['PY_CONNECTION_STR']",
               "engine = create_engine(conn_str)",
               "",
               "df.to_sql('cancer', engine, index=False, if_exists='replace')"
             ]
           },
           {
             'name': 'Breast Cancer Dataset 조회',
             'snippet' : [
               "%%sql",
               "",
               "select * from cancer",
               "FETCH FIRST 20 ROWS ONLY"
             ]
           },
           "---"
         ]//end of submenu for Loading Datasets
       },//end of for Loading Datasets
       {
         'name': 'Query',
         'sub-menu':[
           {
             'name':'Test Query',
             'snippet':[
               "%%sql",
               "SELECT sysdate from DUAL"
             ]
           },
           {
             'name':'Simple Query-Fetch 20',
             'snippet':[
               "%%sql",
               "select * from <TABLE_NAME>",
               "FETCH FIRST 20 ROWS ONLY"
             ]
           },
           {
             'name':'Inline Query-Fetch 20',
             'snippet':[
               "rowcount=20",
               "%sql select * from <TABLE_NAME> FETCH FIRST :rowcount ROWS ONLY"
             ]
           },
           {
             'name':'Inline Query + Python',
             'snippet':[
               "rowcount=20",
               "result = %sql select * from <TABLE_NAME> FETCH FIRST :rowcount ROWS ONLY",
               "result"
             ]
           },
           {
             'name':'Inline Query + Pandas',
             'snippet':[
               "rowcount=20",
               "result = %sql select * from <TABLE_NAME> FETCH FIRST :rowcount ROWS ONLY",
               "df = result.DataFrame()",
               "df.head()"
             ]
           }
         ]
       },
       {
         'name': 'OML',
         'sub-menu': [
           {
             'name':'Explain Table',
             'snippet':[
               "%%script",
               "",
               "BEGIN",
               "    EXECUTE IMMEDIATE 'DROP TABLE <explain_table_name>';",
               "    EXCEPTION WHEN OTHERS THEN NULL;",
               "END;",
               "/",
               "",
               "BEGIN",
               "    DBMS_PREDICTIVE_ANALYTICS.EXPLAIN(",
               "        data_table_name     => '<target_table_name>',",
               "        explain_column_name => '<target_column>',",
               "        result_table_name   => '<explain_table_name>');",
               "END;",
               "/",
             ]
           },
           {
             'name':'Query Explain Table',
             'snippet':[
               "%%sql",
               "",
               "SELECT attribute_name, round(explanatory_value,4), rank",
               "FROM <explain_table_name>",
               "ORDER BY rank, attribute_name",
             ]
           },
           "---",
           {
             'name':'View for Train',
             'snippet':[
               "%%sql",
               "",
               "CREATE OR REPLACE VIEW <VIEW_NAME_FOR_TRAIN> ",
               "AS SELECT * FROM <target_table_name>' SAMPLE (<data_raion>) SEED (<seed_num>)",
               "ORDER BY rank, attribute_name",
             ]
           },
           {
             'name':'View for Test',
             'snippet':[
               "%%sql",
               "",
               "CREATE OR REPLACE VIEW <VIEW_NAME_FOR_TEST> ",
               "AS SELECT * FROM <target_table_name> ",
               "MINUS ",
               "SELECT * FROM <VIEW_NAME_FOR_TRAIN>",
             ]
           },
           "---",
           {
             'name':'Cleaning old Models',
             'snippet':[
               "%%script",
               "",
               "/*  Model 삭제  */",
               "BEGIN",
               "    DBMS_DATA_MINING.DROP_MODEL('<MODEL_NAME>'); ",
               "    EXCEPTION WHEN OTHERS THEN NULL; ",
               "END;",
               "/",
               "",
               "/*  Setting 테이블 삭제  */ ",
               "BEGIN",
               "    EXECUTE IMMEDIATE 'DROP TABLE <SETTING_TABLE_NAME>'; ",
               "    EXCEPTION WHEN OTHERS THEN NULL; ",
               "END;",
               "/",
               "",
               "/*  DIAG 테이블 삭제  */ ",
               "BEGIN",
               "    EXECUTE IMMEDIATE 'DROP TABLE <DIAG_TABLE_NAME>'; ",
               "    EXCEPTION WHEN OTHERS THEN NULL; ",
               "END;",
               "/",
               ""
             ]
           },
           "---",
           {
             'name':'Creating Setting Table',
             'snippet':[
               "%%sql",
               "",
               "CREATE TABLE <SETTING_TABLE_NAME> (",
               "    setting_name  VARCHAR2(30),",
               "    setting_value VARCHAR2(4000)",
               ")"
             ]
           },
           {
             'name':'Setting Parameter for Model(GLR)',
             'snippet':[
               "%%script",
               "",
               "BEGIN",
               "    INSERT INTO <SETTING_TABLE_NAME> (setting_name, setting_value) ",
               "    VALUES(dbms_data_mining.algo_name, ",
               "           dbms_data_mining.algo_generalized_linear_model);",
               "",
               "    INSERT INTO <SETTING_TABLE_NAME> (setting_name, setting_value) ",
               "    VALUES(dbms_data_mining.glms_diagnostics_table_name,  ",
               "           '<DIAG_TABLE_NAME>');",
               "",
               "    INSERT INTO <SETTING_TABLE_NAME> (setting_name, setting_value) ",
               "    VALUES(dbms_data_mining.prep_auto, ",
               "           dbms_data_mining.prep_auto_on);",
               "",
               "    INSERT INTO <SETTING_TABLE_NAME> (setting_name, setting_value) ",
               "    VALUES(dbms_data_mining.glms_ftr_selection, ",
               "           dbms_data_mining.glms_ftr_selection_enable);",
               "",
               "    INSERT INTO <SETTING_TABLE_NAME> (setting_name, setting_value) ",
               "    VALUES(dbms_data_mining.glms_ftr_generation, ",
               "           dbms_data_mining.glms_ftr_generation_enable);",
               "",
               "    --특정 컬럼 가중치 설정",
               "    --INSERT INTO  <SETTING_TABLE_NAME> (setting_name, setting_value) " ,
               "    --VALUES (dbms_data_mining.odms_row_weight_column_name , '<COLUMN_NAME>')" ,
               "",
               "    --Missing Value 처리 옵션 , 기본 값: Average",
               "    --INSERT INTO  <SETTING_TABLE_NAME> (setting_name, setting_value) ",
               "    --VALUES (dbms_data_mining.odms_missing_value_treatment,  ",
               "    --        dbms_data_mining.odms_missing_value_delete_row);",
               "",
               "    -- Regularization: Ridge(L2)",
               "    --INSERT INTO  <SETTING_TABLE_NAME> (setting_name, setting_value) ",
               "    --VALUES (dbms_data_mining.glms_ridge_regression, dbms_data_mining.glms_ridge_reg_enable);",
               "END;",
               "/",
             ]
           },
           {
             'name':'Creating&Running Model',
             'snippet':[
               "%%script",
               "",
               "declare",
               "    v_xlst dbms_data_mining_transform.TRANSFORM_LIST;",
               "BEGIN",
               "    DBMS_DATA_MINING.CREATE_MODEL(",
               "      model_name          => '<MODEL_NAME>',",
               "      mining_function     => <dbms_data_mining.regression>,",
               "      data_table_name     => '<TRAING_TABLE_NAME>',",
               "      case_id_column_name => '<KEY_COLUMN>',",
               "      target_column_name  => '<TARGET_COLUMN>',",
               "      settings_table_name => '<SETTING_TABLE_NAME>',",
               "      xform_list          => v_xlst);",
               "END;",
               "/",
             ]
           },
           "---",
           {
             'name':'Views for Model',
             'snippet':[
               "%%sql",
               "",
               "SELECT view_name, view_type FROM user_mining_model_views",
               "WHERE model_name=upper('<MODEL_NAME>')",
               "ORDER BY view_name",
             ]
           },
           {
             'name':'Diagnostics View for Model',
             'snippet':[
               "%%sql",
               "",
               "select name, numeric_value, string_value",
               "from DM$VG<MODEL_NAME>",
               "ORDER BY view_name"
             ]
           },
           {
             'name':'Parameter View for Model',
             'snippet':[
               "%%sql",
               "",
               "SELECT setting_name, setting_value,model_name",
               "FROM user_mining_model_settings",
               "WHERE model_name = Upper('<MODEL_NAME>')",
               "ORDER BY setting_name"
             ]
           },
           {
             'name':'Applying Model to Test Data',
             'snippet':[
               "%%sql",
               "",
               "create or replace view <TEST_VIEW>_APPLY",
               "as",
               "SELECT SEQ, PREDICTION(<MODEL_NAME> USING *) pr, MEDV, MEDV - PREDICTION(<MODEL_NAME> USING *) residual",
               "FROM <TEST_VIEW>",
             ]
           },
           "---",
         ]//end of submenu for OML
       }//end of for OML
    ] //end of submenu for oci-cli
  };
  //var adw_submenu = adw['sub-menu'];
  //adw_submenu.push(ocicli);
  snippets_menu.options['menus'] = snippets_menu.default_menus;
  snippets_menu.options['menus'].push(ocicli);
  snippets_menu.options['menus'].push(adw);
  console.log('Loaded `snippets_menu` customizations from `custom.js`');
});
