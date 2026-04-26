# Docker stack (Proyecto IA Dental)

Este documento describe el flujo operativo para `docker/docker-compose.yml`, con foco en Kafka, Kafka UI y Logstash.

## 1) Flujo normal

Desde la raiz del proyecto (`C:\Users\pemip\Desktop\Proyecto-ia-dental`):

```powershell
docker compose -f ".\docker\docker-compose.yml" up -d
```

```bash
docker compose -f ./docker/docker-compose.yml up -d
```

Ver estado:

```powershell
docker compose -f ".\docker\docker-compose.yml" ps
```

```bash
docker compose -f ./docker/docker-compose.yml ps
```

## 2) Comprobaciones rapidas

Servicios y URLs:

- Kafka UI: `http://localhost:8085`
- Kibana: `http://localhost:5601`
- Grafana: `http://localhost:3000`
- Elasticsearch: `http://localhost:9200`
- Node-RED: `http://localhost:1880`

Logs utiles:

```powershell
docker compose -f ".\docker\docker-compose.yml" logs kafka --tail=200
docker compose -f ".\docker\docker-compose.yml" logs kafka-ui --tail=200
docker compose -f ".\docker\docker-compose.yml" logs logstash --tail=200
```

```bash
docker compose -f ./docker/docker-compose.yml logs kafka --tail=200
docker compose -f ./docker/docker-compose.yml logs kafka-ui --tail=200
docker compose -f ./docker/docker-compose.yml logs logstash --tail=200
```

## 3) Recuperacion cuando Kafka falla por `Invalid cluster.id`

Si en logs de Kafka aparece algo como:

`Invalid cluster.id in: /var/lib/kafka/data/meta.properties`

el `cluster.id` guardado en `./docker/data/kafka` no coincide con el estado actual de `./docker/data/zookeeper`.

### Opcion recomendada (rapida): reset de datos Kafka + Zookeeper

> Aviso: este proceso elimina metadatos y topicos persistidos de Kafka.

Comando unico recomendado:

```powershell
powershell -ExecutionPolicy Bypass -File ".\docker\recover-kafka-zk.ps1"
```

```bash
bash ./docker/recover-kafka-zk.sh
```

Opcional (WSL/Git Bash): hacerlo ejecutable para lanzarlo sin `bash`.

```bash
chmod +x ./docker/recover-kafka-zk.sh
./docker/recover-kafka-zk.sh
```

Opciones utiles:

```powershell
# Simula sin tocar nada
powershell -ExecutionPolicy Bypass -File ".\docker\recover-kafka-zk.ps1" -DryRun

# Omite backup previo (mas rapido, menos seguro)
powershell -ExecutionPolicy Bypass -File ".\docker\recover-kafka-zk.ps1" -NoBackup
```

```bash
# Simula sin tocar nada
bash ./docker/recover-kafka-zk.sh --dry-run

# Omite backup previo (mas rapido, menos seguro)
bash ./docker/recover-kafka-zk.sh --no-backup
```

Atajo rapido con alias (Bash/WSL):

```bash
# Solo sesion actual
alias recover-kafka='bash ./docker/recover-kafka-zk.sh'
recover-kafka --dry-run

# Persistente
echo "alias recover-kafka='bash /mnt/c/Users/pemip/Desktop/Proyecto-ia-dental/docker/recover-kafka-zk.sh'" >> ~/.bashrc
source ~/.bashrc
```

Si prefieres hacerlo de forma manual:

```powershell
docker compose -f ".\docker\docker-compose.yml" stop kafka kafka-ui zookeeper
docker compose -f ".\docker\docker-compose.yml" rm -f kafka kafka-ui zookeeper
Remove-Item -Path ".\docker\data\kafka" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\docker\data\zookeeper" -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path ".\docker\data\kafka" -Force | Out-Null
New-Item -ItemType Directory -Path ".\docker\data\zookeeper" -Force | Out-Null
docker compose -f ".\docker\docker-compose.yml" up -d zookeeper kafka kafka-ui
```

```bash
docker compose -f ./docker/docker-compose.yml stop kafka kafka-ui zookeeper
docker compose -f ./docker/docker-compose.yml rm -f kafka kafka-ui zookeeper
rm -rf ./docker/data/kafka
rm -rf ./docker/data/zookeeper
mkdir -p ./docker/data/kafka
mkdir -p ./docker/data/zookeeper
docker compose -f ./docker/docker-compose.yml up -d zookeeper kafka kafka-ui
```

Validacion posterior:

```powershell
docker compose -f ".\docker\docker-compose.yml" ps
docker compose -f ".\docker\docker-compose.yml" logs kafka --tail=120
docker compose -f ".\docker\docker-compose.yml" logs kafka-ui --tail=120
```

```bash
docker compose -f ./docker/docker-compose.yml ps
docker compose -f ./docker/docker-compose.yml logs kafka --tail=120
docker compose -f ./docker/docker-compose.yml logs kafka-ui --tail=120
```

## 4) Logstash: pipeline minimo esperado

La carpeta `./docker/data/logstash_pipeline` debe contener al menos un `.conf`.

Archivo minimo incluido: `docker/data/logstash_pipeline/logstash.conf`.

Si modificas pipelines, reinicia Logstash:

```powershell
docker compose -f ".\docker\docker-compose.yml" restart logstash
docker compose -f ".\docker\docker-compose.yml" logs logstash --tail=200
```

```bash
docker compose -f ./docker/docker-compose.yml restart logstash
docker compose -f ./docker/docker-compose.yml logs logstash --tail=200
```

## 5) Parar el stack

```powershell
docker compose -f ".\docker\docker-compose.yml" down
```

```bash
docker compose -f ./docker/docker-compose.yml down
```

Si necesitas borrar tambien volúmenes/datos asociados por Compose:

```powershell
docker compose -f ".\docker\docker-compose.yml" down -v
```

```bash
docker compose -f ./docker/docker-compose.yml down -v
```

