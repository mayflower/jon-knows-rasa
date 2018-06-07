FROM python:3.6

RUN mkdir -p /mnt/bot && mkdir /mnt/bot/data && mkdir /mnt/bot/models
WORKDIR /mnt/bot

COPY config plugin actions.py config.py nlu_model.py dialogue_model.py create_models.sh requirements.txt /mnt/bot/
RUN pip install -r requirements.txt && pip install sklearn_crfsuite spacy && python -m spacy download de && python -m spacy link de de && ./mnt/bot/create_models.sh

CMD ["errbot", "config.py"]