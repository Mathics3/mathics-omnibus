FROM ubuntu:jammy

ENV MATHICS_HOME=/usr/src/app

ENV ASY_VERSION=asymptote-2.83

ENV ENTRYPOINT_COMMAND="docker run -it {MATHICS_IMAGE}"
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
WORKDIR $MATHICS_HOME

COPY requirements.txt ./
RUN apt-get update
RUN apt-get install -qq apt-utils

# We don't need inkscape for convering image logos to PDFs
# Instead we will copy these from the outside.
# # Install inkscape for running TeX doc. It is is in its own PPA.
# RUN apt-get install -qq software-properties-common
# RUN add-apt-repository ppa:inkscape.dev/stable
# RUN apt-get install -qq inkscape

# we need libsqlite3-dev now if ubuntu doesn't come with that, we'll need
# to build our own Python

# inxi and mesa-utils might be optional
# npm pulls in nodejs, but we'll be explicit.

RUN apt-get update -y && apt-get upgrade -y -qq

# Install lots of packages
RUN apt-get install -y -qq \
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
    pkg-config \
    remake \
    rustc \
    sqlite3 \
    tesseract-ocr \
    texlive-fonts-recommended \
    tk8.6-blt2.5 \
    xserver-xorg-video-all

# # Set up Pyston
# COPY src/*_amd64.deb /tmp/
# RUN dpkg -i /tmp/*_amd64.deb

# to make docker layers be more usuable in development
# defer deletion until close to the end
# RUN rm -fr /tmp*_amd64.deb

RUN apt-get install -y -qq python3 python3-pip

ENV PYTHON=python3
ENV PIP=pip3
RUN $PYTHON -m pip install --upgrade pip
# COPY src/*.py3-none-any.whl src/*pyston_23*.whl /tmp/
# RUN $PIP install wheel /tmp/*.py3-none-any.whl /tmp/*pyston_23*.whl
RUN $PIP install --no-cache-dir -r requirements.txt

####################################################
# Mathics scanner
####################################################

# We need to do this until the next release
RUN git clone https://github.com/Mathics3/mathics-scanner.git src/mathics-scanner
RUN (cd src/mathics-scanner && make)

################
# Mathics core #
################

RUN git clone https://github.com/Mathics3/mathics-core
RUN (cd mathics-core && make)

RUN apt-get install -y -qq librsvg2-bin pyqt5-dev-tools

# We need newer versions of Asymptote and GhostScript for bulding the PDF
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y -qq freeglut3 libfftw3-double3 libglew2.2 libsigsegv2 ghostscript imagemagick texlive-pstricks
COPY ubuntu-bin/gs /usr/local/bin/

#--
# build new version of Asymptote for our docs and for inside mathicsscript. The Ubuntu-distributed asymptote has bugs.
#--
RUN apt-get install -y -qq \
  autoconf \
  bison \
  file \
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

####################################################
# Mathics core docs
####################################################

ENV DATA_DIR=/usr/src/app/mathics-core/mathics/doc/latex/
ENV DOC_LATEX_DATA_PCL=/usr/src/app/mathics-core/mathics/doc/latex/doc_latex_data.pcl
ENV DOC_LATEX_DIR=/usr/src/app/mathics-core/mathics/doc/latex/
ENV DOC_LATEX_FILE=/usr/src/app/mathics-core/mathics/doc/latex/documentation.tex
ENV DOC_USER_HTML_DATA_PATH=/usr/src/app/mathics-core/mathics/doc/latex/doc_html_data.pcl

COPY tex-images/*.pdf src/mathics-core/mathics/doc/latex/
RUN ls -l src/mathics-core/mathics/doc/latex/
ENV DOC_LATEX_FILE=/usr/src/app/mathics-core/mathics/doc/latex/documentation.tex
# COPY src/documentation.tex mathics-core/mathics/doc/latex/documentation.tex
RUN ls -l src/mathics-core/mathics/doc/latex/
RUN (cd mathics-core/mathics/doc/latex && DOC_TEX_DATA_PATH=/usr/src/app/mathics-core/mathics/doc/latex/doc_tex_data.pcl PYTHON=$PYTHON remake -x texdoc || /bin/true)
RUN ls -l src/mathics-core/mathics/doc/latex/

####################################################
# Mathics Pymathics and Pymathics Graph for Django #
####################################################

RUN $PIP install -e git+https://github.com/Mathics3/pymathics-graph#egg=pymathics-graph
RUN $PIP install -e git+https://github.com/Mathics3/pymathics-natlang#egg=pymathics-natlang
RUN ${PYTHON} -m spacy download en_core_web_sm
RUN ${PYTHON} -m nltk.downloader wordnet omw-1.4

##################
# Mathics Django #
##################
RUN $PYTHON -m pip install -e git+https://github.com/Mathics3/mathics-django#egg=Mathics-Django[full]

RUN (cd src/mathics-django && PIP=$PIP make)
# We need -ok since we what Unicode in PCL but tests assume ASCII
RUN (cd src/mathics-django && $PYTHON mathics_django/docpipeline.py -ok --want-sorting) || true
RUN mkdir -p /usr/src/app/.local/var/mathics && cp -v $DOC_USER_HTML_DATA_PATH /usr/src/app/.local/var/mathics/doc_data.pcl

##################
# Mathicsscript  #
##################

# # Mathicsscript loses functionality with pyston because matplotlib doesn't render
# # images with it
# # Install python 3.10 packages
# RUn apt-get install -qq -y \
#    python3 \
#    python3-click \
#    python3-cryptography \
#    python3-cson \
#    python3-dateutil \
#    python3-matplotlib \
#    python-matplotlib-data \
#    python3-numpy \
#    python3-pip \
#    python3-psutil \
#    python3-pyqt5 \
#    python3-pyqt5.qtsvg \
#    python3-setuptools \
#    python3-sympy

# ENV PYTHON=/usr/bin/python3
# ENV PIP=pip3
# RUN $PYTHON -m pip install --upgrade pip
# RUN $PIP install /tmp/*.py3-none-any.whl
COPY requirements-mathicsscript.txt ./
RUN $PIP install --no-cache-dir -r requirements-mathicsscript.txt
# RUN $PIP install git+https://github.com/Mathics3/mathics-core.git#egg=Mathics3[full]

#########################################################
# Mathics Pymathics and Pymathics Graph for mathicsscript
# RUN $PIP install -e git+https://github.com/Mathics3/pymathics-graph#egg=pymathics-graph
# RUN $PIP install -e git+https://github.com/Mathics3/pymathics-natlang#egg=pymathics-natlang
RUN ${PYTHON} -m spacy download en_core_web_sm
RUN ${PYTHON} -m nltk.downloader wordnet omw-1.4

# prompt toolkit needs an IPython that is newer than what got
# implicitly installed above
RUN ${PYTHON} -m pip install 'ipython>=7.23.1'

# RUN ${PYTHON} -m pip install mathicsscript[full]
RUN ${PYTHON} -m pip install -e git+https://github.com/Mathics3/mathicsscript#egg=mathicsscript[full]
RUN (cd src/mathicsscript && make)

##################
# debug stuff    #
##################
RUN apt-get install -y -qq emacs
RUN pip install trepan3k

##################
# Finish up      #
##################

# Cleanup
RUN rm -fr /tmp*_amd64.deb /tmp/*.whl

COPY entrypoint.sh /usr/local/bin/mathics-omnibus.sh
RUN chmod +x /usr/local/bin/mathics-omnibus.sh
RUN ln -vs /usr/local/bin/mathicsserver /usr/bin/mathicsserver

EXPOSE 8000

RUN groupadd mathics && \
    useradd -d $MATHICS_HOME -g mathics -m -s /bin/bash mathics && \
    mkdir -p $MATHICS_HOME/data && \
    chown -R mathics:mathics $MATHICS_HOME

COPY django-db/mathics.sqlite /usr/src/app/.local/var/mathics/mathics.sqlite
RUN chown -v -R mathics:mathics /usr/src/app/.local/var/mathics/mathics.sqlite

USER mathics

# # RUN ${PYTHON} -m spacy download en_core_web_sm
# # RUN ${PYTHON} -m nltk.downloader wordnet omw-1.4

ENTRYPOINT ["/usr/local/bin/mathics-omnibus.sh"]

CMD ["--help"]
