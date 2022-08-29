FROM registry.fedoraproject.org/fedora:35
LABEL maintainer="Red Hat"

WORKDIR /src
RUN dnf -y install \
    --setopt=deltarpm=0 \
    --setopt=install_weak_deps=false \
    --setopt=tsflags=nodocs \
    golang \
    gcc \
    git-core-2.32.0 \
    python3-devel \
    python3-pip \
    python3-setuptools \
    strace \
    https://kojipkgs.fedoraproject.org//packages/golang/1.17/2.fc36/noarch/golang-src-1.17-2.fc36.noarch.rpm \
    https://kojipkgs.fedoraproject.org//packages/golang/1.17/2.fc36/x86_64/golang-1.17-2.fc36.x86_64.rpm \
    https://kojipkgs.fedoraproject.org//packages/golang/1.17/2.fc36/x86_64/golang-bin-1.17-2.fc36.x86_64.rpm \
    && dnf clean all

COPY . .

RUN pip3 install -r requirements.txt --no-deps --no-cache-dir --require-hashes

ENTRYPOINT ["python3", "main.py"]
