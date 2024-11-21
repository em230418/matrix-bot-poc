FROM registry.altlinux.org/alt/alt:p10
USER root

RUN apt-get update

RUN apt-get install -y \
    git \
    python3 \
    python3-module-pip

RUN python3 -m pip install \
    matrix-nio

CMD ["./main.py"]
