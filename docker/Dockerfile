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
# npm pulls in nodejs, but we'll be explicit.

# Install lots of packages
RUN DEBIAN_FRONTEND="noninteractive" TZ="US/Eastern" apt-get install -qq liblapack-dev llvm-12 llvm-12-dev gfortran maria libmysqlclient-dev sqlite3 python3-pip python3-setuptools git python3-numpy python3-matplotlib python-matplotlib-data x11-apps latexmk texlive-xetex lmodern texlive-latex-extra texlive-fonts-recommended nodejs npm xserver-xorg-video-all libgl1-mesa-glx libgl1-mesa-dri mesa-utils evince gyp

RUN pip install --no-cache-dir -r requirements.txt
COPY requirements-mathicsscript.txt ./
RUN pip install --no-cache-dir -r requirements-mathicsscript.txt

################
# Mathics core #
################
RUN pip install "Mathics3[full]>=4.0.0"
# RUN pip install git+git://github.com/mathics/Mathics.git#egg=Mathics3[full]

# RUN DEBIAN_FRONTEND="noninteractive" TZ="US/Eastern" apt-get install -qq librsvg2-bin python3-cson python3-pyqt5 python3-pyqt5.qtsvg

# We need newer versions of Asymptote and GhostScript for bulding the PDF
# COPY ubuntu-dpkg/*.deb /tmp/
# RUN dpkg --install /tmp/libgc1_8.0.4-3_amd64.deb /tmp/libgsl25_2.6+dfsg-2_amd64.deb /tmp/libgslcblas0_2.6+dfsg-2_amd64.deb
# RUN DEBIAN_FRONTEND="noninteractive" TZ="US/Eastern" apt-get install -qq freeglut3 libfftw3-double3 libglew2.1 libsigsegv2 ghostscript imagemagick texlive-pstricks
# RUN dpkg --install /tmp/asymptote_2.70+ds-2_amd64.deb
# COPY ubuntu-bin/gs /usr/local/bin/

# Skip building PDF and just copy it to the place entrypoint.sh
# expects it.
COPY tex-images/mathics.pdf /usr/src/app/data/mathics.pdf

#####################
# Mathics Pymathics #
#####################

RUN pip install pymathics-graph

# natlang installs spacy so this should come first
RUN pip install pymathics-natlang
RUN ${PYTHON} -m spacy download en
RUN ${PYTHON} -m nltk.downloader wordnet omw

##################
# Mathicsscript  #
##################

# prompt toolkit needs an IPython that is newer than what got
# implicitly installed above
RUN ${PYTHON} -m pip install 'ipython<8.0,>=7.23.1'
RUN ${PYTHON} -m pip install mathicsscript[full]


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
