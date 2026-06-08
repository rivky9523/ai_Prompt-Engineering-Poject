FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash coreutils \
    && useradd -m runner \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/runner

# copy runner script into container as root, make it executable, then drop privileges
COPY runner.sh /home/runner/runner.sh
RUN chmod +x /home/runner/runner.sh && chown runner:runner /home/runner/runner.sh

USER runner

ENTRYPOINT ["/home/runner/runner.sh"]
