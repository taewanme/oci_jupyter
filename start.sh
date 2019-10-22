docker stop ociml
docker rm ociml
docker run -idt 
-p 8888:8888 
-v /Users/taewan/taewanme_lab/tw_project/jupyter/test:/root/ipython   \
--name ociml  \
ociml2:0.1.1

#ociml:0.1

#

#