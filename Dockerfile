FROM hitokizzy/geezram:slim-buster

RUN git clone -b main https://github.com/ayrizz/Nay /home/ubot/
WORKDIR /home/ubot

RUN wget https://raw.githubusercontent.com/ayrizz/Naya/naya/requirements.txt \
    && pip3 install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt \
    && rm requirements.txt
CMD bash start
