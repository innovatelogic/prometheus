FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-24.04 AS prometeus-base

# Install clang, llvm, git, and gtest
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        clang \
        libclang-dev \
        llvm \
        llvm-dev \
        build-essential \
        git \
        cmake \
        libgtest-dev \
        libbenchmark-dev \
        build-essential \
        libopencv-dev \
        python3 \
        python3-dev \
        python3-venv \
        python3-pip \
        python3-numpy \
        libgnutls28-dev \
        libboost-all-dev && \
    # Build and install gtest
    cd /usr/src/gtest && \
    cmake . && \
    make && \
    cp lib/*.a /usr/lib && \
    # Clean up to reduce the image size
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install --break-system-packages pytest sympy matplotlib ninja


# ---------- Stage 1: Build Seastar ----------
FROM prometeus-base AS seastar-builder

WORKDIR /build

COPY build-seastar.sh ./build-seastar.sh
RUN chmod +x ./build-seastar.sh
RUN sudo ./build-seastar.sh

# ---------- Stage 2: Final Dev Container ----------
FROM prometeus-base

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
RUN pip3 install -r requirements.txt --ignore-installed --break-system-packages

# Copy Seastar installed files from builder
COPY --from=seastar-builder /usr/local/include /usr/local/include
COPY --from=seastar-builder /usr/local/lib /usr/local/lib
COPY --from=seastar-builder /usr/local/lib/pkgconfig /usr/local/lib/pkgconfig

ENV LD_LIBRARY_PATH="/usr/local/lib:/workspaces/prometheus/build/bin" \
    CPLUS_INCLUDE_PATH="/usr/local/include:$CPLUS_INCLUDE_PATH" \
    PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH" \
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

CMD ["bash"]
