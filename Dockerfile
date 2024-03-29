FROM python:3.11 as builder

WORKDIR /wg-node-build

# install pdm (https://github.com/pdm-project/pdm)
RUN pip install -U pip setuptools wheel pdm

# copy project files
COPY pyproject.toml pdm.lock* ./
COPY wg_node ./wg_node


# install dependencies and project into the local packages directory
RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

FROM python:3.11-alpine as runner

WORKDIR /wg-node

# retrieve packages from build stage
COPY --from=builder /wg-node-build/__pypackages__/3.11/lib ./packages/
COPY --from=builder /wg-node-build/wg_node ./wg_node

ENV PYTHONPATH=/wg-node/packages

# install necessary packages
RUN apk add -U --no-cache wireguard-tools dumb-init

EXPOSE 51820/udp
EXPOSE 51821/tcp
EXPOSE 8080

ENTRYPOINT ["dumb-init", "python", "-m", "uvicorn", "wg_node.main:app", "--host", "0.0.0.0", "--port", "8080"]
