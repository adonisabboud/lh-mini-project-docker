FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ansible \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ansible && \
    mkdir -p /home/ansible/.ssh && \
    echo "Host *\n    StrictHostKeyChecking no" > /home/ansible/.ssh/config && \
    chmod 700 /home/ansible/.ssh && \
    chmod 600 /home/ansible/.ssh/config && \
    chown -R ansible:ansible /home/ansible

USER ansible
WORKDIR /home/ansible

CMD ["/bin/bash"]