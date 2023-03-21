# """
# Koopa fetch and run image.
# @author Michael Steinbaugh
# @note Updated 2023-03-20.
# """

FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9c8f-main
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
USER root
RUN python3 -m pip install 'latch==2.14.0' \
 && mkdir -pv '/opt/latch' \
 && apt-get update \
 && apt-get \
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
 && curl -sSL 'https://koopa.acidgenomics.com/install' \
    | bash -s -- --non-interactive --verbose \
 && koopa install conda \
 && koopa system info
COPY . /root/
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
CMD ["bash", "-il"]
