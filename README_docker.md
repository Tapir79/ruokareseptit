# Luo docker image

##  Asenna Buildx builder ja lataa QEMU emulattorit
```
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap   # QEMU 
```

## Tagit
```
IMAGE=tapir79/ruokareseptit
TAG=latest           
```

## Lisää Dockerhubiin
```
docker buildx build \
  --platform linux/amd64,linux/arm64/v8 \
  -t ${IMAGE}:${TAG} \
  --push \
  .
```

## Intel / x86 host
```
docker pull ${IMAGE}:${TAG}      # linux/amd64 variant
```
Esim:
```
docker pull tapir79/ruokareseptit
```

## Apple‑silicon Mac
```
docker pull ${IMAGE}:${TAG}      # linux/arm64 variant
```

## Tarkista arkkitehtuuri
```
docker image inspect ${IMAGE}:${TAG} --format '{{.Os}}/{{.Architecture}}'
```
Esim:
```
docker image inspect tapir79/ruokareseptit --format '{{.Os}}/{{.Architecture}}'
```

## Käynnistä image

Pysyvä tietokanta bind‑mount
```
docker run -p 5000:5000 \
  -v "$PWD/database/database.db:/app/database.db" \
  ${IMAGE}:${TAG}
```

Esim:

```
docker run -p 5000:5000 -v "$PWD/database/database.db:/app/database.db" tapir79/ruokareseptit
```