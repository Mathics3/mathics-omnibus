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
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -qq liblapack-dev llvm-12 llvm-12-dev llvm-11 llvm-11-dev gfortran maria libmysqlclient-dev sqlite3 python3-pip python3-setuptools git python3-numpy python3-matplotlib python-matplotlib-data x11-apps latexmk texlive-xetex lmodern texlive-latex-extra texlive-fonts-recommended nodejs npm xserver-xorg-video-all libgl1-mesa-glx libgl1-mesa-dri mesa-utils evince gyp libffi7 libopenblas-dev rustc libxslt1-dev libxml2-dev cargo

# Pyston
COPY src/libssl1.1_1.1.1l-1ubuntu1.6_amd64.deb .
RUN DEBIAN_FRONTEND="noninteractive" dpkg -i ./libssl1.1_1.1.1l-1ubuntu1.6_amd64.deb
COPY src/pyston_2.3.4_20.04_amd64.deb /tmp/
RUN dpkg -i /tmp/pyston_2.3.4_20.04_amd64.deb
ENV PYTHON=pyston
COPY src/*.whl /tmp/
RUN pip-pyston install /tmp/*.whl

RUN pip install --no-cache-dir -r requirements.txt
COPY requirements-mathicsscript.txt ./
RUN pip install --no-cache-dir -r requirements-mathicsscript.txt
COPY ubuntu-dpkg/*.deb /tmp/

################
# Mathics core #
################
# RUN pip install "Mathics3[full]>=4.0.0"
RUN pip install git+https://github.com/Mathics3/mathics-core.git#egg=Mathics3[full]

RUN DEBIAN_FRONTEND="noninteractive" apt-get install -qq librsvg2-bin python3-cson python3-pyqt5 python3-pyqt5.qtsvg pyqt5-dev-tools

# We need newer versions of Asymptote and GhostScript for bulding the PDF
RUN dpkg --install /tmp/libgc1_8.0.4-3_amd64.deb /tmp/libgsl25_2.6+dfsg-2_amd64.deb /tmp/libgslcblas0_2.6+dfsg-2_amd64.deb
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -qq freeglut3 libfftw3-double3 libglew2.2 libsigsegv2 ghostscript imagemagick texlive-pstricks
COPY ubuntu-bin/gs /usr/local/bin/

#--
# build new version of Asymptote for our docs and for inside mathicsscript. The Ubuntu-distributed asymptote has bugs.
#--
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -qq autoconf libgc-dev bison flex libreadline-dev libcurl4 texinfo libsigsegv2 libcurl4 libcurl3-gnutls libcurl4-gnutls-dev libgl-dev freeglut3-dev libglm-dev
COPY src/${ASY_VERSION}.src.tgz .
RUN tar -xpf ${ASY_VERSION}.src.tgz
RUN (cd ${ASY_VERSION} && bash ./autogen.sh && ./configure --disable-lsp && make -j3 all && make -j3 install)

RUN git clone https://github.com/Mathics3/mathics-core.git
ENV DATA_DIR=/usr/src/app/mathics-core/mathics/doc/tex/
ENV DOC_USER_TEX_DATA_PATH=/usr/src/app/mathics-core/mathics/doc/tex/doc_tex_data.pcl
ENV DOC_USER_HTML_DATA_PATH=/usr/src/app/mathics-core/mathics/doc/tex/doc_html_data.pcl

COPY tex-images/*.pdf mathics-core/mathics/doc/tex/
ENV DOC_LATEX_FILE=/usr/src/app/mathics-core/mathics/doc/tex/documentation.tex
RUN (cd mathics-core && ${PYTHON} ./setup.py develop)
RUN (cd mathics-core && make texdoc || /bin/true)

# #####################
# # Mathics Pymathics #
# #####################

RUN pip-pyston install pymathics-graph
RUN pip-pyston install /tmp/spacy-3.4.0-pyston38-pyston_23_x86_64_linux_gnu-linux_x86_64.whl

RUN pip-pyston install pymathics-natlang
RUN ${PYTHON} -m spacy download en
RUN ${PYTHON} -m nltk.downloader wordnet omw

##################
# Mathics Django #
##################
RUN ${PYTHON} -m pip install -e git+https://github.com/Mathics3/mathics-django@graphics3d-fixup#egg=Mathics-Django[full]

RUN (cd src/mathics-django && make)
RUN (cd src/mathics-django && ${PYTHON} mathics_django/docpipeline.py -ok) || true
RUN mkdir -p /usr/src/app/.local/var/mathics && cp -v $DOC_USER_HTML_DATA_PATH /usr/src/app/.local/var/mathics/doc_data.pcl

# ##################
# # Mathicsscript  #
# ##################

ENV PYTHON=/usr/bin/python3.10
RUN pip install git+https://github.com/Mathics3/mathics-core.git#egg=Mathics3[full]
RUN pip install pymathics-graph
## Something is funky with spacy, so skip for now
## RUN pip install pymathics-natlang

# prompt toolkit needs an IPython that is newer than what got
# implicitly installed above
RUN ${PYTHON} -m pip install 'ipython>=7.23.1'

# RUN ${PYTHON} -m pip install mathicsscript[full]
RUN ${PYTHON} -m pip install -e git+https://github.com/Mathics3/mathicsscript#egg=mathicsscript[full]
RUN (cd src/mathicsscript && make)

##################
# debug stuff    #
##################
RUN apt-get install -qq emacs
RUN pip install trepan3k

##################
# Finish up      #
##################
COPY entrypoint.sh /usr/local/bin/mathics.sh
RUN chmod +x /usr/local/bin/mathics.sh

EXPOSE 8000

RUN groupadd mathics && \
    useradd -d $MATHICS_HOME -g mathics -m -s /bin/bash mathics && \
    mkdir -p $MATHICS_HOME/data && \
    chown -R mathics:mathics $MATHICS_HOME

USER mathics
COPY django-db/mathics.sqlite /usr/src/app/.local/var/mathics/mathics.sqlite

ENTRYPOINT ["/usr/local/bin/mathics.sh"]

CMD ["--help"]
