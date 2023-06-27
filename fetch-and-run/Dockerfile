# """
# Koopa fetch and run image.
# @author Michael Steinbaugh
# @note Updated 2023-06-27.
# """

FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:5303-main
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
USER root
RUN /usr/local/bin/python3 -m pip install \
        -vvv \
        --disable-pip-version-check \
        --no-cache-dir \
        --upgrade \
        'latch' \
 && /bin/mkdir -pv '/opt/latch' \
 && /usr/bin/apt-get update \
 && /usr/bin/apt-get \
        --no-install-recommends \
        --yes \
        install \
            'bash' \
            'ca-certificates' \
            'coreutils' \
            'curl' \
            'findutils' \
            'git' \
            'locales' \
            'lsb-release' \
            'perl' \
            'procps' \
            'sudo' \
            'unzip' \
 && /usr/bin/apt-get clean \
 && /bin/rm -fr '/var/lib/apt/lists/'* \
 && /usr/bin/curl -sSL 'https://koopa.acidgenomics.com/install' \
    | /bin/bash -s -- --non-interactive --verbose \
 && /opt/koopa/bin/koopa system info
COPY . /root/
WORKDIR /root
CMD ["/bin/bash", "-il"]
