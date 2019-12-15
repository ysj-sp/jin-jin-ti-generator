FROM python:3.7.4
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install cython
RUN pip install --no-cache-dir -r requirements.txt

RUN gdown https://drive.google.com/uc?id=1B-eD0SclQyAVue2sBAjwYblquVRgqmrJ
RUN mkdir saved_model && cd saved_model && gdown https://drive.google.com/uc?id=1mUlZSLcg_qbN532Cbn7QjY2fEGhFhQmG

COPY . .
RUN cd utils && python download_model.py
RUN rm -rf utils/data.zip

CMD [ "python", "predict.py" ]
