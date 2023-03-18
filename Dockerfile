FROM hitokizzy/geezram:slim-buster

RUN git clone -b naya https://github.com/Onlymeriz/Naya /home/ubot/
WORKDIR /home/ubot

RUN wget https://raw.githubusercontent.com/Onlymeriz/Naya/naya/requirements.txt?token=GHSAT0AAAAAACAHBMEVV76PBORO7EQSXR52ZAWC32A\
    && pip3 install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt \
    && rm requirements.txt
CMD bash start
