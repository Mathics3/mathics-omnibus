FROM ubuntu:focal

ENV TZ=US/Eastern
ENV MATHICS_HOME=/usr/src/app
ENV ENTRYPOINT_COMMAND="docker run -it {MATHICS_IMAGE}"
ENV PYTHON=python3

WORKDIR $MATHICS_HOME

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY requirements.txt ./
RUN apt-get update
RUN apt-get install -qq apt-utils

# we need libsqlite3-dev now if ubuntu doesn't come with that, we'll need
# to build our own Python
# Leave out inkscape  for now.

# inxi and mesa-utils might be optional
# npm puls in nodejs, but we'll be explicit.
# llvm-11 and llvm-11-dev might work?

# Install lots of packages
RUN DEBIAN_FRONTEND="noninteractive" TZ="US/Eastern" apt-get install -qq liblapack-dev llvm-10 llvm-10-dev gfortran maria libmysqlclient-dev sqlite3 python3-pip python3-setuptools git python3-numpy python3-matplotlib python-matplotlib-data x11-apps asymptote w3m latexmk texlive-xetex lmodern texlive-latex-extra texlive-fonts-recommended nodejs npm xserver-xorg-video-all libgl1-mesa-glx libgl1-mesa-dri mesa-utils evince

RUN pip install --no-cache-dir -r requirements.txt
COPY requirements-mathicsscript.txt ./
RUN pip install --no-cache-dir -r requirements-mathicsscript.txt

################
# Mathics core #
################
RUN pip install "Mathics3[full]>=3.1.0"

#####################
# Mathics Pymathics #
#####################

RUN pip install pymathics-natlang
RUN pip install pymathics-graph

##################
# Mathicsscript  #
##################

RUN ${PYTHON} -m pip install -e mathicsscript[full]

RUN ${PYTHON} -m nltk.downloader wordnet omw
RUN ${PYTHON} -m spacy download en

##################
# Mathics Django #
##################
RUN ${PYTHON} -m pip install Mathics-Django[full]

##################
# debug stuff    #
##################
# RUN apt-get install -qq emacs
# RUN pip install trepan3k

##################
# Finish up      #
##################
EXPOSE 8000

RUN groupadd mathics && \
    useradd -d $MATHICS_HOME -g mathics -m -s /bin/bash mathics && \
    mkdir -p $MATHICS_HOME/data && \
    chown -R mathics:mathics $MATHICS_HOME

USER mathics
COPY django-db/mathics.sqlite /usr/src/app/.local/var/mathics/mathics.sqlite

ENTRYPOINT ["/entrypoint.sh"]

CMD ["--help"]
