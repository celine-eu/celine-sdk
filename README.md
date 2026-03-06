# celine-sdk

Shared CELINE SDK:

- Versioned OpenAPI specs under `openapi/<service>/v<version>/openapi.json`
- Generated OpenAPI clients under `celine.sdk.openapi.<package>`
- Shared infrastructure:
  - OIDC token providers (`celine.sdk.auth`)
  - MQTT broker abstraction (`celine.sdk.broker`)
  - Pydantic settings (`celine.sdk.settings`)
  

## CLI

```bash
# fetch and version specs (writes to ./openapi)
celine-sdk spec fetch services.yaml

# list discovered versions
celine-sdk spec list

# generate clients (requires: pip install 'celine-sdk[gen]')
celine-sdk generate services.yaml
```

## services.yaml

```yaml
services:
  digital-twin:
    package: dt
    openapi: http://dt:8000/openapi.json
  policies:
    openapi: http://policies:8000/openapi.json
```

```bash
# fetch and version specs (writes to ./openapi)
celine-sdk spec fetch services.yaml

# list discovered versions
celine-sdk spec list

# generate clients (requires: pip install 'celine-sdk[gen]')
celine-sdk generate services.yaml
```

## services.yaml

```yaml
services:
  digital-twin:
    package: dt
    openapi: http://dt:8000/openapi.json
  policies:
    openapi: http://policies:8000/openapi.json
```
