FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04

RUN apt-get update -y && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    add-apt-repository -y ppa:ubuntugis/ppa -y && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        clang \
        libclang-dev \
        llvm \
        llvm-dev \
        build-essential \
        git \
        cmake \
        pkg-config \
        checkinstall \
        python3.10 \
        python3.10-dev \
        python3.10-venv \
        libsm6 \
        libxext6 \
        python3-pip \
        python3.9-distutils \
        python3-numpy \
        gdal-bin \
        libgdal-dev \
        libgeographic-dev \
        libboost-all-dev \
        libgtest-dev \
        libgtkmm-3.0-dev \
        libgstreamermm-1.0-dev \
        libbenchmark-dev \
        curl \
        wget \
        unzip \
        patchelf \
        libxml2 \
        libxml2-dev \
        libjpeg62 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
    update-alternatives --set python /usr/bin/python3.10 && \
    python -m pip install --upgrade setuptools pip distlib && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

WORKDIR /workspaces/prometheus

# Copy package files and install Node.js dependencies
COPY package.json package-lock.json ./

RUN npm install node-fetch ws socket.io-client@4 --save \
    && npm install --save-dev @types/node-fetch @types/ws

# Copy Python requirements and install
COPY requirements.txt ./
RUN apt update && apt install -y python3 python3-pip
RUN pip3 install -r requirements.txt --ignore-installed

ENV LD_LIBRARY_PATH="/workspaces/prometheus/build/bin" \
    PROMETHEUS_APP_DATA="/workspaces/prometheus/runtime" \
    PYTHONPATH="/workspaces/prometheus/srv" \
    FLASK_APP="driver:create_app" \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8088


ARG USERNAME=vscode
RUN id -u ${USERNAME} &>/dev/null || useradd -m ${USERNAME}

RUN echo "kernel.yama.ptrace_scope = 0" > /etc/sysctl.d/99-ptrace.conf && \
    chmod 644 /etc/sysctl.d/99-ptrace.conf && \
    sysctl --system

CMD ["bash"]: