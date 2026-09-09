
# expolore image
docker run --rm -it judge0-custom:1.13.1 bash
ls -la /usr/local/python-3.12.13/
ls -d /usr/local/python-*
/usr/local/python-3.12.13/bin/python3 --version


# expolore container
docker exec -it judge0-v1131-workers-1 bash
which node
node --version
ls -l $(which node)
echo $PATH


# Update JavaScript version inside judge0 container.
docker build --no-cache -t judge0-custom:1.13.1 .
docker run --rm judge0-custom:1.13.1 /usr/local/node-22.19.0/bin/node --version


# create Dockerfile
FROM judge0/judge0:1.13.1

USER root

RUN curl -fsSL https://www.python.org/ftp/python/3.12.13/Python-3.12.13.tgz \
    -o /tmp/python.tgz \
    && tar -xzf /tmp/python.tgz -C /tmp \
    && cd /tmp/Python-3.12.13 \
    && ./configure --prefix=/usr/local/python-3.12.13 --enable-optimizations \
    && make -j"$(nproc)" \
    && make install \
    && rm -rf /tmp/Python-3.12.13 /tmp/python.tgz

RUN curl -fsSL https://nodejs.org/dist/v22.19.0/node-v22.19.0-linux-x64.tar.xz \
    -o /tmp/node.tar.xz \
    && mkdir -p /usr/local/node-22.19.0 \
    && tar -xJf /tmp/node.tar.xz \
    -C /usr/local/node-22.19.0 \
    --strip-components=1 \
    && rm /tmp/node.tar.xz

USER judge0


# restart conatiners
docker compose down
docker compose up -d



# login to judge0 postgres db bash
docker exec -it judge0-v1131-db-1 psql -U judge0 -d judge0

SELECT id, name, run_cmd
FROM languages
WHERE id = 63;

UPDATE languages
SET
    name = 'JavaScript (Node.js 22.19.0)',
    run_cmd = '/usr/local/node-22.19.0/bin/node script.js'
WHERE id = 63;

UPDATE languages
SET
    name = 'Python (3.12.13)',
    run_cmd = '/usr/local/python-3.12.13/bin/python3 script.py'
WHERE id = 71;



# free docker disk space
docker system df -v
docker builder prune -a
docker system df
docker image ls



