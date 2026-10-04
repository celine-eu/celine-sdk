# CHANGELOG

## Unreleased

<!-- Hand-written ahead of the release. semantic-release inserts the next version
     below the marker and leaves this section in place: remove it when releasing.
     Entries shipped in v1.23.0 were removed from here; the `import_yaml` fix's code
     shipped in v1.23.0 too, and `74d7e7e` added its tests. -->

### Features

- `celine.sdk.posture` (REQ-0180–0183): the platform's one deployment-posture rule. Signal
  `CELINE_ENV`, then `ENVIRONMENT`, then a caller's legacy names; **only `dev` relaxes**,
  unset or any other value is hardened. `PostureGuard` collects a service's development
  defaults (dev database password, client secret equal to the client id, the SDK's own
  issuer/JWKS defaults, dev switches) and raises `InsecureConfiguration` once, listing all
  of them, outside `dev`. Every service adopting it needs this release.

### Breaking changes

- **A platform grant is the realm role `platform-admin`; realm groups grant nothing**
  (REQ-0042). New in `celine.sdk.auth`: `PLATFORM_ADMIN_ROLE`, `realm_roles(claims)` (reads
  `realm_access.roles` only), `is_platform_admin(claims)`, and `Grants` (`.platform`,
  `.in_org(alias)`, `.is_platform_admin`, `.aliases`), plus `JwtUser.realm_roles`,
  `JwtUser.is_platform_admin` and `JwtUser.grants`. `organization_groups(claims, alias)` and
  `organization_aliases(claims)` stay.
- **Removed `extract_groups` and `realm_groups`.** The first merged the realm `groups` claim
  with every organization's groups, which made a community's `admins` a platform
  administrator in dataset-api (NIS2 R1); the second read realm groups as platform grants.
  Migrate platform checks to `is_platform_admin` and organization checks to
  `organization_groups` / `Grants.in_org` for the organization the request is about.
- **`celine.sdk.policies.Subject` has `roles: list[str]`** (default empty), and the engine
  emits it as `input.subject.roles` (REQ-0042, REQ-0056). Fill it with
  `realm_roles(user.claims)`; Rego checks `"platform-admin" in input.subject.roles`. The
  subject document now always has six keys. Services that added `roles` themselves (a
  `Subject` subclass, a `_build_input` override, or setting `["subject"]["roles"]` on the
  built dict) keep working and can drop the workaround.
- **Regenerated `celine.sdk.openapi.onboarding`: `AdminMe.realm_groups` is now
  `AdminMe.platform_roles`** (the caller's realm roles; `GET /api/admin/me`), generated from
  the new snapshot `openapi/onboarding/v0.5.0/` (onboarding `info.version` 0.5.0);
  `openapi/onboarding/v0.4.0/` is unchanged from its release. Also new at 0.5.0 (additive):
  submission revisions (list, record, and `POST …/revisions/{revision_id}/retry` with its own
  body `RevisionRetryRequest`), shared delivery points, `declared_existing_member` and the
  consent document URLs and hashes on the submission models, and every `ConsentCreate` field
  now optional. `RetryRequest` stays the enablement retry's body. The generator's numbered
  `schemas.LocaleSchema2` is now `LocaleSchema3` (no consumer in the workspace names either).
- **`JwtUser.has_role(role)` reads realm roles** (`realm_access.roles`) and lost its
  `claim_key` argument; it used to read a top-level `roles` claim, which no platform mapper
  emits. Use `get_claim` for any other claim.

### Security

- `pyjwt>=2.14` (GHSA-ffc3-869f-jxw9, GHSA-9v7f-9g4p-ffgj); lock: pyjwt 2.15.1,
  cryptography 50.0.2, urllib3 2.8.0.

- REC registry: `RecRegistryAdminClient.list_duplicate_delivery_points(community_key, *,
  token=None)` wraps `GET /admin/communities/{community_key}/delivery-points/duplicates`
  (rec-registry 1.7.0; REQ-0136). Answers `DeliveryPointDuplicatesSchema` (now exported
  from `celine.sdk.rec_registry`), the whole list in one call; anything but `200` raises
  `RecRegistryApiError`, including the uncoded `404` for an unknown community.
- Regenerated `celine.sdk.openapi.rec_registry`: the unreleased rec-registry 1.7.0 grew this
  route, so `openapi/rec-registry/v1.7.0/` was updated in place (additive: the operation and
  `DeliveryPointDuplicates`, `DuplicateDeliveryPoint`, `DuplicateHolder`).

<!-- version list -->

## v1.24.0 (2026-10-01)

### Bug Fixes

- Correct yaml import
  ([`74d7e7e`](https://github.com/celine-eu/celine-sdk/commit/74d7e7eea936a2e71ee5d25d7c5e7e94083302ec))

### Features

- List community shared delivery points
  ([`9bacb6f`](https://github.com/celine-eu/celine-sdk/commit/9bacb6f00b6afd1f691992db0d70a9af579cb037))


## v1.23.0 (2026-10-01)

### Features

- Wrap participant update, per-field member writes and delivery-point replace/delete
  ([`82fedc0`](https://github.com/celine-eu/celine-sdk/commit/82fedc042ec5d86138fa42b79b98dddde56e488b))


## v1.22.0 (2026-09-29)

### Documentation

- Update specs
  ([`c27b4bc`](https://github.com/celine-eu/celine-sdk/commit/c27b4bc58659a05adb3a4cbc40463368222d95b2))

### Features

- Update onboarding api
  ([`ec9e69d`](https://github.com/celine-eu/celine-sdk/commit/ec9e69d927c865a1a63d81c778fa9ebc8a0b0b98))


## v1.21.0 (2026-09-28)

### Features

- Update api signature
  ([`85f9265`](https://github.com/celine-eu/celine-sdk/commit/85f92652d15e176aea1dad245bad4d6ef52aa6ef))

- Update rec registry, onboarding APIs
  ([`919afa7`](https://github.com/celine-eu/celine-sdk/commit/919afa779ad0722e6d695e87de50c47a9a0c8f45))

- Update registry api
  ([`b6d6ba2`](https://github.com/celine-eu/celine-sdk/commit/b6d6ba2132ca72af2ae0a461d1f5bf78a64ab765))


## v1.20.0 (2026-09-14)

### Features

- Regen for onboarding
  ([`e16017b`](https://github.com/celine-eu/celine-sdk/commit/e16017bcc2045ee12925f56a7170fee434355f9d))

- Update rec registry create signature
  ([`aa908f8`](https://github.com/celine-eu/celine-sdk/commit/aa908f8d492866422c61ece6debbd3c5b34d6a57))


## v1.19.0 (2026-09-14)

### Features

- Review provisioning api, add email invitation
  ([`e8c5578`](https://github.com/celine-eu/celine-sdk/commit/e8c5578fdf44acb2ecc7a8eea863f8e19f6b9d90))


## v1.18.0 (2026-09-14)

### Features

- Add provisioning API
  ([`9ada16c`](https://github.com/celine-eu/celine-sdk/commit/9ada16c4a2b5a459c4b714cf66a01934ebb3fd60))

- Upgrade provisioning signature
  ([`6058fc2`](https://github.com/celine-eu/celine-sdk/commit/6058fc28be9fa9f7c3e7f757294a2269437f189c))


## v1.17.3 (2026-09-11)

### Bug Fixes

- Improve organization claim management
  ([`725e795`](https://github.com/celine-eu/celine-sdk/commit/725e795e98241b64464bd912039c5823b66d5415))


## v1.17.2 (2026-09-11)

### Bug Fixes

- Added the Manager Dashboard
  ([`f4cbbd5`](https://github.com/celine-eu/celine-sdk/commit/f4cbbd51c748e344364a80267788ef70d7a3bffa))


## v1.17.1 (2026-09-08)

### Bug Fixes

- **nudging**: Restore Facts model dropped by regen; tolerate non-contract ingest error bodies
  ([`dbc7a7d`](https://github.com/celine-eu/celine-sdk/commit/dbc7a7daa01c91f523e6dcf141b74762e8185e8f))


## v1.17.0 (2026-09-07)

### Bug Fixes

- Regen onboarding v0.2
  ([`7c304e8`](https://github.com/celine-eu/celine-sdk/commit/7c304e80b781e55905bee3bf40019eb37a3f3993))

### Features

- Add onboarding API
  ([`477d239`](https://github.com/celine-eu/celine-sdk/commit/477d239b81d97bb497f2fddd02aafd0a0716cc81))


## v1.16.0 (2026-08-31)

### Bug Fixes

- Add limit and error handling to rec registry, closes #41
  ([`604075f`](https://github.com/celine-eu/celine-sdk/commit/604075f3e07104a27e1b82580339d95788d17481))

### Chores

- Update workflows
  ([`4f4a39d`](https://github.com/celine-eu/celine-sdk/commit/4f4a39dce04d7723034e55c7e4b3a1ba9b6f02fe))

- Update workfow image version
  ([`f09a232`](https://github.com/celine-eu/celine-sdk/commit/f09a232e4a6f52f3dd1d1d9e3fb21fad267c63c9))

### Features

- Regenerate api, update harness
  ([`351f638`](https://github.com/celine-eu/celine-sdk/commit/351f638fbc7aef57c43302b199ed4dd3c3bf823c))

- Update rec regisrty v0.6
  ([`67c539e`](https://github.com/celine-eu/celine-sdk/commit/67c539e07debd8cf4ffe9388723a66cb73cb776e))


## v1.15.0 (2026-08-13)

### Features

- Add rec-registry lookup by ids
  ([`ce4641b`](https://github.com/celine-eu/celine-sdk/commit/ce4641b88d3a8c6720a01b6a5013b35f06744978))

- Expose rec registry api
  ([`14670a1`](https://github.com/celine-eu/celine-sdk/commit/14670a18a9c658b37f4981fe3c8b72d082f30aa4))

- Review python version boundaries
  ([`d0dbf8a`](https://github.com/celine-eu/celine-sdk/commit/d0dbf8a433f2449f98259592ce571285e5a1f186))


## v1.14.1 (2026-07-20)

### Bug Fixes

- Notification language, add info button
  ([`14c1964`](https://github.com/celine-eu/celine-sdk/commit/14c1964bef9d02598ee604b3afe93c52b7d2d1b2))


## v1.14.0 (2026-07-03)

### Features

- **flexibility**: Regenerate models for community-first suggestions (nullable impact/reward,
  community_kwh)
  ([`4db4940`](https://github.com/celine-eu/celine-sdk/commit/4db4940c3112549466c78b86f19102c34e41fd80))


## v1.13.0 (2026-07-02)

### Chores

- **deps**: Bump cachetools
  ([`81233ae`](https://github.com/celine-eu/celine-sdk/commit/81233ae1ac6aa20d2b7ed50987dcf368fff824e7))

- **deps**: Bump pydantic from 2.12.5 to 2.13.0
  ([`89b61c1`](https://github.com/celine-eu/celine-sdk/commit/89b61c137ca7811013c89fa28c60ec53bcdf79f2))

- **deps-dev**: Bump pytest
  ([`7089e73`](https://github.com/celine-eu/celine-sdk/commit/7089e73742866bc88027fe15d3dab772262a9ddb))

### Continuous Integration

- Bump pypa/gh-action-pypi-publish
  ([`a0c3f06`](https://github.com/celine-eu/celine-sdk/commit/a0c3f06794bcdd0227ddb27088367777e61ee146))

### Features

- Add ai_assistant wrapper
  ([`8bbae59`](https://github.com/celine-eu/celine-sdk/commit/8bbae592635c0a615de481759a92378e6f4e4eda))

- Add group extraction for realm/organization
  ([`66d8755`](https://github.com/celine-eu/celine-sdk/commit/66d875586c0ca5f01b5225fb10a3b9bff4e204d5))


## v1.12.1 (2026-04-27)

### Bug Fixes

- Add grid list indext
  ([`42dd758`](https://github.com/celine-eu/celine-sdk/commit/42dd758b907788d9aa67fdf11164fc3a10cb8498))


## v1.12.0 (2026-04-27)

### Features

- Add nowcasting api client call
  ([`2244911`](https://github.com/celine-eu/celine-sdk/commit/22449112c76050b0ac7eac46049b94f422e0fada))


## v1.11.0 (2026-04-22)

### Features

- Improve grid wrapper, use value fetchers vs custom routes
  ([`fc8efe6`](https://github.com/celine-eu/celine-sdk/commit/fc8efe6af7fb57d993534e4515e0753260b1b192))


## v1.10.0 (2026-04-16)

### Chores

- Add AGENTS.md
  ([`36e7df4`](https://github.com/celine-eu/celine-sdk/commit/36e7df441b14272c1b68b9b12778ee7230c022fa))

### Features

- Update flexibility api
  ([`bdea704`](https://github.com/celine-eu/celine-sdk/commit/bdea704252c994df00bbb03dfdcd702db0e9d355))


## v1.9.0 (2026-04-13)

### Features

- Add notification control
  ([`6c6e43b`](https://github.com/celine-eu/celine-sdk/commit/6c6e43b14d5c0ea5e5f6affd4959475823319247))


## v1.8.0 (2026-04-12)

### Chores

- **deps**: Bump attrs from 25.4.0 to 26.1.0
  ([`1921282`](https://github.com/celine-eu/celine-sdk/commit/1921282e0a1099c6492eb922eb60d7e8bf595e64))

- **deps**: Bump pyjwt from 2.11.0 to 2.12.1
  ([`c923ae8`](https://github.com/celine-eu/celine-sdk/commit/c923ae80f0a798bf8c2e4ae2c306cbe022288d31))

### Continuous Integration

- Bump hynek/build-and-inspect-python-package in the actions group
  ([`721f155`](https://github.com/celine-eu/celine-sdk/commit/721f155558c9864a74b1872b81cd19229e7c5dd3))

### Features

- Add flex api export
  ([`0c3a541`](https://github.com/celine-eu/celine-sdk/commit/0c3a5416666a96fe61e803cd68c044f0ac4a2afb))


## v1.7.0 (2026-04-11)

### Chores

- Add grid poc
  ([`da6f84e`](https://github.com/celine-eu/celine-sdk/commit/da6f84efe3001aba1fd78363d64ca76223af5d75))

- **deps**: Bump pydantic-settings from 2.12.0 to 2.13.0
  ([`c4b52a0`](https://github.com/celine-eu/celine-sdk/commit/c4b52a04e3dea71bf1f35b0bebc63bf08e251392))

- **deps**: Bump the runtime-dependencies group across 1 directory with 3 updates
  ([`f757340`](https://github.com/celine-eu/celine-sdk/commit/f757340268becf7ee2febdb7d6fbe7bd3752e163))

- **deps-dev**: Bump openapi-python-client
  ([`a53752e`](https://github.com/celine-eu/celine-sdk/commit/a53752e920fb5ae60f040db6b9da6de06ab4a516))

### Continuous Integration

- Bump the actions group across 1 directory with 2 updates
  ([`8906f6a`](https://github.com/celine-eu/celine-sdk/commit/8906f6a2ca2733220a64e41a1f8772249b312081))

### Features

- Add grid poc
  ([`d507062`](https://github.com/celine-eu/celine-sdk/commit/d5070622b67db380b403d0117260c6d074a256e7))

- Add openapi client updates
  ([`e26b1bf`](https://github.com/celine-eu/celine-sdk/commit/e26b1bf3f070eb3bdf00087db37609da65ab9b71))

- Add organization support
  ([`396747f`](https://github.com/celine-eu/celine-sdk/commit/396747f9976562a35138fdfca3073cacd561816d))

- Refactor to new rec registry import/export API
  ([`a35e648`](https://github.com/celine-eu/celine-sdk/commit/a35e648c1f4ef4f6f7296a4767c6e216e6ec2227))

- Update openapi
  ([`3e48644`](https://github.com/celine-eu/celine-sdk/commit/3e486445cf04207b368852520d08d9a2030cd23e))


## v1.6.0 (2026-04-05)

### Features

- Add flexibility api
  ([`fa1717e`](https://github.com/celine-eu/celine-sdk/commit/fa1717eb7bfe087d08e16d4652d9558381b4daa2))


## v1.5.0 (2026-04-03)

### Features

- Add dt commitment api call
  ([`3d7e70e`](https://github.com/celine-eu/celine-sdk/commit/3d7e70e73933a1bbf7100b2bad5abbc696aeb6d5))

- Update openapi, add ontology methods to DT client
  ([`84a87e7`](https://github.com/celine-eu/celine-sdk/commit/84a87e71deba0e4d077c1d3387f9cef9e8f84f68))


## v1.4.3 (2026-03-21)

### Bug Fixes

- Correct types, regen api
  ([`403fa99`](https://github.com/celine-eu/celine-sdk/commit/403fa9955521583f3a826fac4f9ffae36516e141))


## v1.4.2 (2026-03-06)

### Bug Fixes

- Release
  ([`1ede3ea`](https://github.com/celine-eu/celine-sdk/commit/1ede3ea3c6653bc35879377369689472df222a12))


## v1.4.1 (2026-03-02)

### Bug Fixes

- Expose JwtUser.get_username
  ([`b82522a`](https://github.com/celine-eu/celine-sdk/commit/b82522a78fba04c2caab0b7bbcdfc074943033ce))


## v1.4.0 (2026-02-28)

### Features

- Add verify_ssl flag
  ([`bbe21f6`](https://github.com/celine-eu/celine-sdk/commit/bbe21f6c922cee377b3b7ab95330701a4153b522))


## v1.3.1 (2026-02-27)

### Bug Fixes

- Update regours
  ([`5ca0fe1`](https://github.com/celine-eu/celine-sdk/commit/5ca0fe1a3ae0b61a47e1d58d081bf1dff0602348))

### Chores

- Upgrade taskfile with setup
  ([`6fa02fd`](https://github.com/celine-eu/celine-sdk/commit/6fa02fd2ef322925d26399b9408d0601e2fa2103))


## v1.3.0 (2026-02-23)

### Features

- Add nudging client
  ([`45e7758`](https://github.com/celine-eu/celine-sdk/commit/45e77589e97c11da97c49a419f61ffa211cedb76))

- Upgrade rec registry api, update wrapper
  ([`ac678c5`](https://github.com/celine-eu/celine-sdk/commit/ac678c5e0ff2c38bebbc64484c1bc44e541cb036))


## v1.2.1 (2026-02-20)

### Bug Fixes

- Improve setting, logging
  ([`d4f76ac`](https://github.com/celine-eu/celine-sdk/commit/d4f76acb6d13bbc29893967eb8331f27b75b26fa))


## v1.2.0 (2026-02-19)

### Chores

- Update regoruse
  ([`c6a188e`](https://github.com/celine-eu/celine-sdk/commit/c6a188e5e2d3a0563fd3fccefeafe76b45f09d55))

### Features

- Improve mqtt reconnection
  ([`0d424fe`](https://github.com/celine-eu/celine-sdk/commit/0d424fe0451cd230b04f9cbb4bb8b1bedb05cd4e))

- Improve oidc token refresh, force mqtt reconnect on token expiration
  ([`704c279`](https://github.com/celine-eu/celine-sdk/commit/704c2791eeed62600ce1900a40afd75c7d852bb2))


## v1.1.0 (2026-02-16)

### Bug Fixes

- Adapt wrappers
  ([`04bb6d2`](https://github.com/celine-eu/celine-sdk/commit/04bb6d2e44ff253d9c7cdeab3d2593122bf0d17a))

- Corrected return parsing
  ([`da6485a`](https://github.com/celine-eu/celine-sdk/commit/da6485a060801f9151921f53f3116967bb40b7fe))

- Mqtt conn cred, gen sdk
  ([`45520df`](https://github.com/celine-eu/celine-sdk/commit/45520df4f745362fc5dc9673a124995b9ad43648))

- Typed response
  ([`1665ead`](https://github.com/celine-eu/celine-sdk/commit/1665eadc2f4032afe37dc6efd30b1536ebd49510))

### Chores

- Regen clients
  ([`3442be6`](https://github.com/celine-eu/celine-sdk/commit/3442be6a8da459d7e39ed04f4315b2b50e0390de))

- Updare rec registry
  ([`3628969`](https://github.com/celine-eu/celine-sdk/commit/3628969b64c653754f3a3e4392035bbead530e82))

- Update registry api
  ([`2326617`](https://github.com/celine-eu/celine-sdk/commit/2326617e635ddfa5cb8e49769146f816d83d1638))

### Continuous Integration

- Bump actions/checkout from 6.0.1 to 6.0.2 in the actions group
  ([`2a319fe`](https://github.com/celine-eu/celine-sdk/commit/2a319fe53ee296a49117899df866c9d1c05dacdc))

### Features

- Normalize jwt parsing from oidc settings
  ([`112794d`](https://github.com/celine-eu/celine-sdk/commit/112794d1549e900321f16a81652f8743b0401e79))

- Review dt api
  ([`d541884`](https://github.com/celine-eu/celine-sdk/commit/d54188496c69c1e93ee048ea07da71e5c921aba9))

- Update api, adapt wrappers
  ([`fc76119`](https://github.com/celine-eu/celine-sdk/commit/fc761193fd52ab336021642a7d7c3ed9fdd0a65d))


## v1.0.1 (2026-02-02)

### Bug Fixes

- Skip duplicate checks
  ([`f648ca5`](https://github.com/celine-eu/celine-sdk/commit/f648ca5bdaddf4663f4ad1989d8c2006855c9123))


## v1.0.0 (2026-02-02)

- Initial Release
