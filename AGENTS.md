## Repository role

This repo contains the Celine SDK python API.

## Structure

`src/celine/sdk` provides the client API to interact with CELINE services. 

- `./openapi` folder is READ ONLY, generated via `task gen`. When modifying the SDK take care to not edit the `openapi` subpackage and instead ask the user to update the generated clients.
- `./mqtt` has the MQTT client
- `./auth` provides OIDC based authentication (`OidcClientCredentialsProvider`, `StaticTokenProvider`), JWT model parsing  (`JwtUser`)
- `./policies` handles OPA interface over local services `*.rego`

there are then dedicated modules wrapping the openapi clients (e.g. `flexibility`, `rec_registry`) that offers the public API wrappers to simplify interaction.
