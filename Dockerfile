FROM cennznet/cennznet:1.2.0 AS build


FROM debian:stretch-slim
LABEL maintainer="support@centrality.ai"

RUN apt-get update && apt-get install -y ca-certificates openssl python3 python3-pip && \
	  mkdir -p /root/.local/share/cennznet && \
      ln -s /root/.local/share/cennznet /data && \
	  groupadd -g 1000 cennznet && \
	  useradd -ms /bin/bash -u 1000 -g 1000 cennznet

COPY --from=0 /usr/local/bin/cennznet /usr/local/bin/
COPY --from=0 /cennznet/genesis/ /cennznet/genesis/

COPY main_work.py /usr/local/bin/
RUN chmod +x /usr/local/bin/main_work.py

EXPOSE 30333 9933 9944
VOLUME ["/data"]

ENTRYPOINT ["/usr/local/bin/main_work.py"]
