FROM python:3.10

ARG USER_ID
ARG GROUP_ID

WORKDIR /code

RUN groupadd --gid ${GROUP_ID} resumer \
    && useradd \
      --uid ${USER_ID} \
      --gid ${GROUP_ID} \
      --create-home \
      --home-dir /code \
      --shell /bin/bash \
      resumer \
    && chown -R resumer:resumer /code

RUN DEBIAN_FRONTEND=noninteractive apt-get update -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq wkhtmltopdf \
    && pip install -U pip setuptools wheel poetry \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY --chown=resumer:resumer requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=resumer:resumer resume/ ./resume/
COPY --chown=resumer:resumer configs/ ./configs/
COPY --chown=resumer:resumer content/ ./content/
#COPY --chown=resumer:resumer README.txt .
#COPY --chown=resumer:resumer CHANGES.txt .
COPY --chown=resumer:resumer setup.py .

RUN pip install . \
    && chown -R resumer:resumer /code

RUN apt-get update && apt install fonts-open-sans

USER resumer

EXPOSE 6543
CMD pserve configs/resume.ini
