FROM ubuntu:jammy

ENV MATHICS_HOME=/usr/src/app

###  The Asymptote mess ###
# asymptote version 2.78 is known into work inside docker for mathicsscript while 2.79
# does not. Asymptote is also used in PDF generation and here newer versions are generally
# better for that.
ENV ASY_VERSION=asymptote-2.78

ENV ENTRYPOINT_COMMAND="docker run -it {MATHICS_IMAGE}"
WORKDIR $MATHICS_HOME

COPY requirements.txt ./
RUN apt-get update
RUN apt-get install -qq apt-utils

# we need libsqlite3-dev now if ubuntu doesn't come with that, we'll need
# to build our own Python
# Leave out inkscape  for now.

# inxi and mesa-utils might be optional
# npm pulls in nodejs, but we'll be explicit.

# Install lots of packages
RUN DEBIAN_FRONTEND="noninteractive" apt install -y -qq \
    cargo \
    evince \
    gfortran \
    git x11-apps \
    gyp \
    latexmk texlive-xetex \
    libffi7 \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    liblapack-dev \
    libmysqlclient-dev \
    libopenblas-dev \
    libxml2-dev \
    libxslt1-dev \
    llvm-11 \
    llvm-11-dev \
    llvm-12 \
    llvm-12-dev \
    lmodern texlive-latex-extra \
    maria \
    mesa-utils \
    nodejs \
    npm \
    rustc \
    sqlite3 \
    texlive-fonts-recommended \
    tk8.6-blt2.5 \
    xserver-xorg-video-all

# Set up Pyston
COPY src/*_amd64.deb /tmp/
RUN DEBIAN_FRONTEND="noninteractive" dpkg -i /tmp/*_amd64.deb
ENV PYTHON=pyston
COPY src/*.whl /tmp/
RUN pip-pyston install /tmp/*.py3-none-any.whl /tmp/*pyston_23*.whl
RUN pip-pyston install --no-cache-dir -r requirements.txt

################
# Mathics core #
################
# RUN pip install "Mathics3[full]>=4.0.0"
RUN pip-pyston install git+https://github.com/Mathics3/mathics-core.git#egg=Mathics3[full]

RUN apt install -y -qq librsvg2-bin pyqt5-dev-tools

# We need newer versions of Asymptote and GhostScript for bulding the PDF
RUN DEBIAN_FRONTEND="noninteractive" apt install -y -qq freeglut3 libfftw3-double3 libglew2.2 libsigsegv2 ghostscript imagemagick texlive-pstricks
COPY ubuntu-bin/gs /usr/local/bin/

#--
# build new version of Asymptote for our docs and for inside mathicsscript. The Ubuntu-distributed asymptote has bugs.
#--
RUN apt install -y -qq \
  autoconf \
  bison \
  flex \
  freeglut3-dev \
  libcurl3-gnutls \
  libcurl4 \
  libcurl4 \
  libcurl4-gnutls-dev \
  libgc-dev \
  libgl-dev \
  libglm-dev \
  libreadline-dev \
  libsigsegv2 \
  texinfo

COPY src/${ASY_VERSION}.src.tgz .
RUN tar -xpf ${ASY_VERSION}.src.tgz
RUN (cd ${ASY_VERSION} && bash ./autogen.sh && ./configure --disable-lsp && make -j3 all && make -j3 install)

RUN git clone https://github.com/Mathics3/mathics-core.git
ENV DATA_DIR=/usr/src/app/mathics-core/mathics/doc/tex/
ENV DOC_USER_TEX_DATA_PATH=/usr/src/app/mathics-core/mathics/doc/tex/doc_tex_data.pcl
ENV DOC_USER_HTML_DATA_PATH=/usr/src/app/mathics-core/mathics/doc/tex/doc_html_data.pcl

COPY tex-images/*.pdf mathics-core/mathics/doc/tex/
ENV DOC_LATEX_FILE=/usr/src/app/mathics-core/mathics/doc/tex/documentation.tex
RUN (cd mathics-core && pip-pyston install -e .[full])
RUN (cd mathics-core && PYTHON=pyston make texdoc || /bin/true)

# Broken for Mathics 5.x
# ####################################################
# # Mathics Pymathics and Pymathics Graph for Django #

# RUN pip-pyston install pymathics-graph
# pymathics-natlang is current broken
# RUN pip-pyston install pymathics-natlang
# RUN ${PYTHON} -m spacy download en
# RUN ${PYTHON} -m nltk.downloader wordnet omw

##################
# Mathics Django #
##################
RUN pyston -m pip install -e git+https://github.com/Mathics3/mathics-django@graphics3d-fixup#egg=Mathics-Django[full]

RUN (cd src/mathics-django && PIP=pip-pyston make)
RUN (cd src/mathics-django && pyston mathics_django/docpipeline.py -ok) || true
RUN mkdir -p /usr/src/app/.local/var/mathics && cp -v $DOC_USER_HTML_DATA_PATH /usr/src/app/.local/var/mathics/doc_data.pcl

##################
# Mathicsscript  #
##################
# Install python 3.10 packages
RUN DEBIAN_FRONTEND="noninteractive" apt install -y \
   python3 \
   python3-click \
   python3-cryptography \
   python3-cson \
   python3-dateutil \
   python3-matplotlib \
   python-matplotlib-data \
   python3-numpy \
   python3-pip \
   python3-psutil \
   python3-pyqt5 \
   python3-pyqt5.qtsvg \
   python3-setuptools \
   python3-sympy

ENV PYTHON=/usr/bin/python3
RUN pip install /tmp/*.py3-none-any.whl
COPY requirements-mathicsscript.txt ./
RUN pip install --no-cache-dir -r requirements-mathicsscript.txt
RUN pip install git+https://github.com/Mathics3/mathics-core.git#egg=Mathics3[full]

# Broken for Mathics 5.x
# #########################################################
# # Mathics Pymathics and Pymathics Graph for mathicsscript
# RUN pip install pymathics-graph
# RUN pip install pymathics-natlang

# prompt toolkit needs an IPython that is newer than what got
# implicitly installed above
RUN ${PYTHON} -m pip install 'ipython>=7.23.1'

# RUN ${PYTHON} -m pip install mathicsscript[full]
RUN ${PYTHON} -m pip install -e git+https://github.com/Mathics3/mathicsscript#egg=mathicsscript[full]
RUN (cd src/mathicsscript && make)

##################
# debug stuff    #
##################
RUN apt install -y -qq emacs
RUN pip install trepan3k

##################
# Finish up      #
##################
COPY entrypoint.sh /usr/local/bin/mathics-omnibus.sh
RUN chmod +x /usr/local/bin/mathics-omnibus.sh

EXPOSE 8000

RUN groupadd mathics && \
    useradd -d $MATHICS_HOME -g mathics -m -s /bin/bash mathics && \
    mkdir -p $MATHICS_HOME/data && \
    chown -R mathics:mathics $MATHICS_HOME

USER mathics
COPY django-db/mathics.sqlite /usr/src/app/.local/var/mathics/mathics.sqlite

ENTRYPOINT ["/usr/local/bin/mathics-omnibus.sh"]

CMD ["--help"]
