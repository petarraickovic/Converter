FROM python:alpine3.7
ADD API.py /
ADD FileDownloading.py /
ADD FileProcessing.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./API.py