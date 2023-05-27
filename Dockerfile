# BUILD stage:
FROM python:3.11 as builder

WORKDIR /wg-node-build

# install pdm
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy project files
COPY pyproject.toml pdm.lock* ./
COPY wg_node ./wg_node/

# install dependencies and project into the local packages directory
RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

# 2. RUN stage:
FROM python:3.11-alpine as runner

WORKDIR /wg-node

# retrieve packages from build stage
COPY --from=builder /wg-node-build/__pypackages__/3.11/lib ./lib/
ENV PYTHONPATH=/wg-node/lib

RUN apk add -U --no-cache wireguard-tools dumb-init

EXPOSE 51820/udp
EXPOSE 51821/tcp
EXPOSE 8080

ENTRYPOINT ["dumb-init", "python", "-m", "uvicorn", "wg_node.main:app", "--host", "0.0.0.0", "--port", "8080"]