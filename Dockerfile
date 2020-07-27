FROM python
ADD . /restendpoint
WORKDIR /restendpoint
RUN pip install -r requirements.txt