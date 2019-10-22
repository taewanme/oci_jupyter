# OCI Jupyter 

- Docker Container 실행 명령

```
docker stop ociml
docker rm ociml
docker run -idt -p 8888:8888          
-v /Users/base:/root/ipython   \
--name ociml ociml2:0.1.1
```