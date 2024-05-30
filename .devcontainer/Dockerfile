# Ubuntu doesn't have streamlink in apt?
FROM mcr.microsoft.com/vscode/devcontainers/base:debian

RUN echo "deb http://deb.debian.org/debian bookworm-backports main" | sudo tee "/etc/apt/sources.list.d/streamlink.list" && \
    sudo apt update && \
    sudo apt -t bookworm-backports install streamlink -y

# Symlinks
ENV WORK_DIR=/workspaces/Streamlink-Plugin-Fansly
RUN mkdir -p $WORK_DIR

# Link plugin sideload
# ${XDG_DATA_HOME:-${HOME}/.local/share} doesn't work, even with: `USER vscode`?
ENV PLUGINS_DIR=/home/vscode/.local/share/streamlink/plugins
RUN mkdir -p $PLUGINS_DIR
RUN ln -s $WORK_DIR/fansly.py $PLUGINS_DIR/fansly.py 

# Link config
ENV CONFIG_DIR=/home/vscode/.config/streamlink
RUN mkdir -p $CONFIG_DIR
RUN touch $WORK_DIR/fansly.config
RUN ln -s $WORK_DIR/fansly.config $CONFIG_DIR/config.fansly