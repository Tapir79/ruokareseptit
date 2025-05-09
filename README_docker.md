# Create a docker image

## (1 time only) create & bootstrap a buildx builder
```
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap   # downloads QEMU emulators
```

## choose tags
```
IMAGE=tapir79/ruokareseptit
TAG=latest           
```

## Push to docker hub
```
docker buildx build \
  --platform linux/amd64,linux/arm64/v8 \
  -t ${IMAGE}:${TAG} \
  --push \
  .
```

## On Intel / x86 host
```
docker pull ${IMAGE}:${TAG}      # pulls linux/amd64 variant
```
Example:
```
docker pull tapir79/ruokareseptit
```

## On Apple‑silicon Mac
```
docker pull ${IMAGE}:${TAG}      # pulls linux/arm64 variant
```

## Check architecture
```
docker image inspect ${IMAGE}:${TAG} --format '{{.Os}}/{{.Architecture}}'
```
Example:
```
docker image inspect tapir79/ruokareseptit --format '{{.Os}}/{{.Architecture}}'
```

## Run

with a persistent DB bind‑mount
```
docker run -p 5000:5000 \
  -v "$PWD/database/database.db:/app/database.db" \
  ${IMAGE}:${TAG}
```

Example:

```
docker run -p 5000:5000 -v "$PWD/database/database.db:/app/database.db" tapir79/ruokareseptit
```