# Offensive agent detection coverage

Reviewed on 2026-11-25 against [offensive.agency agents](https://offensive.agency/agents).

Source: offensive.agency v0.2.0, data under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), with passive data credited to ONYPHE. Signatures are adapted to Plum syntax; these rules do not reproduce the tracker's confidence scoring or attribution.

The catalogue contains 83 agents. All 25 entries with a **How it is detected** section have a Plum rule. Three explicitly requested ARTEX forks have separate product rules. Existing rule UUIDs and vendor/product tags are retained; no second rule is introduced for an existing product.

Every implemented rule emits `proto:http`, `type:c2`, one `vendor:*` and one `product:*`. Here `type:c2` is the requested inventory category for operator consoles and offensive-agent APIs. It does not establish malicious use, implant activity, or operator attribution. Repository owners are used as vendor identifiers when no distinct publisher is established.

HTTP title `text` matches become case-insensitive `.lk` terms; `raw` matches use exact terms. Favicon MD5 values are exact alternatives. Multi-term signatures keep explicit `AND`. Existing stronger signatures are retained alongside compatible additions. No default-port restriction is added. Kritt is deliberately stricter than the tracker substring: exact upstream title `open·kritt` or its favicon, because `kritt` alone also matches unrelated Skritter pages. Both RedAmon favicon variants have byte-verified MD5/SHA-256 and independently calculated Shodan-compatible MMH3 alternatives; Pojun has MMH3 `1045559192` for its current favicon.

ONYPHE `app.data.text`, `app.device` and `component.product` fields are not Plum rule fields. Body-only, request-side User-Agent, process, filesystem and behavioural indicators are not mechanically converted to response headers or generic banner matches. Titles such as **Console** and shared assets cannot identify a specific agent. Existing Cairn title-plus-official-favicon matching is retained; its tracker favicon alternative adds independent asset coverage without a title-only fallback.

ARTEX keeps the approved `Autonomous Penetration Testing Console` substring, with additional branded/localized titles and family favicons. Fork-specific hashes stay in Pojun rather than broadening ARTEX to every Pojun deployment. Shared ARTEX signatures may also match branded forks; a family tag plus a fork tag reflects inheritance, not duplicate rules for one product.

RedAmon: the supplied `http://23.251.136.10:3000/favicon.ico` was byte-identical to the upstream pinned favicon. Its MMH3 (`964522141`) was corroborated by passive MODAT file metadata; MD5 and SHA-256 were calculated from the downloaded bytes. Pojun's current upstream favicon has MD5 `e3359c0c947d1eea350bbbd3d9bd2625` and SHA-256 `3990cc3d5cbfc4fcddaa94dbec6ce97616bfd0e44cae2b5b9187c3d47a50953c`; the other two MD5 variants are documented historical tracker signatures.

Plum validation: the previously approved ARTEX English-title query returned zero matching results across the complete cursor traversal from epoch 0 through 2026-11-25T16:25:39Z (17 pages, final cursor exhausted). This is historical `last_seen` discovery, not a statement about current exposure or validation of every new rule. Tracker host lists and MODAT observations are external evidence, not Plum samples.

## Implemented signatures

| Agent | Rule | Coverage |
| --- | --- | --- |
| [aida](https://offensive.agency/agent/aida) | [aida.yaml](../tags/aida.yaml) | New rule |
| [airecon](https://offensive.agency/agent/airecon) | [airecon.yaml](../tags/airecon.yaml) | New rule |
| [artex](https://offensive.agency/agent/artex) | [c2_artex.yaml](../tags/c2_artex.yaml) | Updated existing rule; UUID preserved |
| [autocve](https://offensive.agency/agent/autocve) | [autocve.yaml](../tags/autocve.yaml) | New rule |
| [bob-research-labs](https://offensive.agency/cluster/bob-research-labs) | [bob-research-labs.yaml](../tags/bob-research-labs.yaml) | New fork-specific rule |
| [bugtraceai](https://offensive.agency/agent/bugtraceai) | [bugtraceai.yaml](../tags/bugtraceai.yaml) | Updated existing rule; UUID preserved |
| [cairn](https://offensive.agency/agent/cairn) | [cairn.yaml](../tags/cairn.yaml) | Updated existing rule; UUID preserved |
| [cyberstrike](https://offensive.agency/agent/cyberstrike) | [cyberstrike.yaml](../tags/cyberstrike.yaml) | Updated existing rule; UUID preserved |
| [cyberstrikeai](https://offensive.agency/agent/cyberstrikeai) | [cyberstrikeai.yaml](../tags/cyberstrikeai.yaml) | Updated existing rule; UUID preserved |
| [decepticon](https://offensive.agency/agent/decepticon) | [decepticon.yaml](../tags/decepticon.yaml) | New rule |
| [hexstrike](https://offensive.agency/agent/hexstrike) | [hexstrike-ai.yaml](../tags/hexstrike-ai.yaml) | Updated existing rule; UUID preserved |
| [luan1aoagent](https://offensive.agency/agent/luan1aoagent) | [luan1aoagent.yaml](../tags/luan1aoagent.yaml) | New rule |
| [neurosploit](https://offensive.agency/agent/neurosploit) | [neurosploit.yaml](../tags/neurosploit.yaml) | New rule |
| [nyxstrike](https://offensive.agency/agent/nyxstrike) | [nyxstrike.yaml](../tags/nyxstrike.yaml) | New rule |
| [open-kritt](https://offensive.agency/agent/open-kritt) | [open-kritt.yaml](../tags/open-kritt.yaml) | New rule |
| [pentagi](https://offensive.agency/agent/pentagi) | [pentagi.yaml](../tags/pentagi.yaml) | Updated existing rule; UUID preserved |
| [pentestswarm](https://offensive.agency/agent/pentestswarm) | [pentestswarm.yaml](../tags/pentestswarm.yaml) | New rule |
| [pojun](https://offensive.agency/cluster/pojun) | [pojun.yaml](../tags/pojun.yaml) | New fork-specific rule |
| [redamon](https://offensive.agency/agent/redamon) | [redamon.yaml](../tags/redamon.yaml) | Updated existing rule; UUID preserved |
| [redcell](https://offensive.agency/agent/redcell) | [redcell.yaml](../tags/redcell.yaml) | New rule |
| [sapper-v2](https://offensive.agency/agent/sapper-v2) | [sapper-v2.yaml](../tags/sapper-v2.yaml) | New rule |
| [scopeweaver](https://offensive.agency/cluster/scopeweaver) | [scopeweaver.yaml](../tags/scopeweaver.yaml) | New fork-specific rule |
| [strix](https://offensive.agency/agent/strix) | [strix.yaml](../tags/strix.yaml) | Updated existing rule; UUID preserved |
| [t3mp3st](https://offensive.agency/agent/t3mp3st) | [t3mp3st.yaml](../tags/t3mp3st.yaml) | New rule |
| [vulnerator-ai](https://offensive.agency/agent/vulnerator-ai) | [vulnerator-ai.yaml](../tags/vulnerator-ai.yaml) | New rule |
| [wormxgpt](https://offensive.agency/agent/wormxgpt) | [wormxgpt.yaml](../tags/wormxgpt.yaml) | New rule |
| [xalgorix](https://offensive.agency/agent/xalgorix) | [xalgorix.yaml](../tags/xalgorix.yaml) | New rule |
| [z3r0](https://offensive.agency/agent/z3r0) | [z3r0.yaml](../tags/z3r0.yaml) | New rule |

## Additional passive checks

The following service observations were retrieved from MODAT on 2026-11-25. Links identify observed endpoints; they are historical evidence, not a request to scan them. Counts represent service records, not unique hosts or product-confidence decisions.

| Agent | Observed endpoint | UTC observation | Title |
| --- | --- | --- | --- |
| aida | [161.97.127.165:8443](https://161.97.127.165:8443/) | 2026-11-25T10:58:12Z | AIDA - AI-Driven Security Assessment |
| airecon | [46.250.231.222:8080](http://46.250.231.222:8080/) | 2026-11-25T13:49:43Z | AIRecon Search |
| autocve | [154.202.127.215:3000](http://154.202.127.215:3000/) | 2026-11-25T16:01:29Z | AutoCVE |
| bob-research-labs | [176.65.132.19:8787](http://176.65.132.19:8787/) | 2026-11-25T16:04:24Z | Bob Research Labs: We're coming to root your server! |
| decepticon | [54.38.98.111:3000](http://54.38.98.111:3000/) | 2026-11-23T19:51:21Z | Decepticon — Autonomous Red Team Platform |
| luan1aoagent | [150.158.46.75:8787](http://150.158.46.75:8787/) | 2026-11-24T05:16:10Z | 鸾鸟渗透智能体 · Agent Workbench |
| nyxstrike | [47.238.159.91:443](https://47.238.159.91:443/) | 2026-11-25T09:55:19Z | NyxStrike |
| open-kritt | [104.236.190.69:443](https://104.236.190.69:443/) | 2026-11-25T12:41:40Z | Skritter Blog < The write way to learn characters |
| pentestswarm | [182.237.2.35:8777](http://182.237.2.35:8777/) | 2026-11-25T15:45:30Z | pentestswarm — AI Penetration Testing Dashboard |
| pojun | [195.54.171.64:8443](https://195.54.171.64:8443/) | 2026-11-25T15:02:02Z | Console |
| sapper-v2 | [186.241.81.56:2333](http://186.241.81.56:2333/) | 2026-11-25T02:36:45Z | sapper — engagement graph |
| scopeweaver | [169.58.110.233:8787](http://169.58.110.233:8787/) | 2026-11-25T16:00:45Z | ScopeWeaver — Autonomous Penetration Testing Console |
| t3mp3st | [162.141.167.40:3333](http://162.141.167.40:3333/) | 2026-11-25T07:44:05Z | T3MP3ST - Command & Control Dashboard |
| vulnerator-ai | [198.2.206.118:9100](http://198.2.206.118:9100/) | 2026-11-21T18:21:19Z | Vulnerator Console |
| wormxgpt | [193.181.221.137:3005](http://193.181.221.137:3005/) | 2026-11-25T13:00:05Z | WormGPT Red Terminal |
| xalgorix | [20.16.180.15:80](http://20.16.180.15:80/) | 2026-11-25T16:45:11Z | Xalgorix — Security Scanner |
| z3r0 | [38.76.196.80:8000](http://38.76.196.80:8000/) | 2026-11-25T08:57:03Z | Z3r0 Console |

No NeuroSploit title sample was returned by MODAT; its signatures remain sourced from the attributed tracker. A combined 28-rule Plum search timed out, so it does not establish positive or negative coverage for these rules. The separate, completed ARTEX traversal above remains the only exhaustive Plum result reported here.

## Entries without a published detection section

These 58 entries were reviewed individually. A local bind address alone is not a reason to reject a rule: an operator can expose a service. However, these pages provide no **How it is detected** response signature to translate. No placeholder or always-false rule is created. Distinct source-verified response fingerprints can be added later; absence of a tracker host is not proof of absence in Plum.

| Agent | Published limitation / exposure context |
| --- | --- |
| [agent-zero](https://offensive.agency/agent/agent-zero) | Web interface published on port 50080 by the provided compose file, with no login unless two variables are set. Several hundred interfaces are reachable online; like Hermes Agent, an exposed interface is an exposed agent, so it is not tracked here. |
| [agentic-bug-hunter](https://offensive.agency/agent/agentic-bug-hunter) | Its dashboard listens on the loopback address (port 8777); nothing else is served. |
| [apex](https://offensive.agency/agent/apex) | A terminal tool; the hosted console is a separate commercial product. |
| [ares](https://offensive.agency/agent/ares) | A command-line tool; nothing is served on the network. |
| [aria-x](https://offensive.agency/agent/aria-x) | Its console listens on 127.0.0.1:8787 by default; no instance was found online. |
| [artemis](https://offensive.agency/agent/artemis) | A command-line tool; nothing is served on the network. |
| [autopentester](https://offensive.agency/agent/autopentester) | No service and no port. |
| [blitzstrike](https://offensive.agency/agent/blitzstrike) | No console; its out-of-band listener is opened for a session only. |
| [breachweave](https://offensive.agency/agent/breachweave) | A local web interface titled "tch-agent"; none was seen online in November 2026. |
| [cai](https://offensive.agency/agent/cai) | Its API listens on the loopback address by default, so a standard install shows nothing on the Internet. |
| [cain](https://offensive.agency/agent/cain) | Nothing is served on the network. |
| [chying-agent](https://offensive.agency/agent/chying-agent) | A dashboard titled "CHYing Agent Dashboard"; none was seen online in November 2026. |
| [claude-red](https://offensive.agency/agent/claude-red) | Files loaded by an assistant; nothing is served on the network. |
| [clearwing](https://offensive.agency/agent/clearwing) | A local web interface titled "Clearwing"; none was seen online in November 2026. |
| [cochise](https://offensive.agency/agent/cochise) | A script that drives a Kali machine over SSH; nothing is served on the network. |
| [codex-redteam-mode](https://offensive.agency/agent/codex-redteam-mode) | It only changes the configuration of an assistant on a workstation. |
| [ctf-agent](https://offensive.agency/agent/ctf-agent) | A command-line tool; nothing is served on the network. |
| [custom-ai-agent](https://offensive.agency/agent/custom-ai-agent) | It lives inside Burp Suite on the tester's machine; its MCP server is local. |
| [cyber-autoagent](https://offensive.agency/agent/cyber-autoagent) | A terminal interface; its observability stack publishes port 3000. |
| [cyber-harness](https://offensive.agency/agent/cyber-harness) | Single binaries; its interface title is just "Cyber", which a passive scan cannot single out. |
| [cybermes](https://offensive.agency/agent/cybermes) | No console in the reviewed source; three pages carrying its name were seen online in November 2026, each with a different title. |
| [darkmoon](https://offensive.agency/agent/darkmoon) | The open-source edition is a command-line tool with no web console. |
| [deadend-cli](https://offensive.agency/agent/deadend-cli) | A command-line tool; nothing is served on the network. |
| [echidna](https://offensive.agency/agent/echidna) | A web interface on a Kali machine; none was seen online in November 2026. |
| [guardian](https://offensive.agency/agent/guardian) | A command-line tool; nothing is served on the network. |
| [h-pentest](https://offensive.agency/agent/h-pentest) | A web console on ports 8000 and 5173; none was seen online in November 2026. |
| [hackingbuddygpt](https://offensive.agency/agent/hackingbuddygpt) | Command line only: the current version has no network service. |
| [hermes-agent](https://offensive.agency/agent/hermes-agent) | Its own dashboard listens on the loopback address (port 9119). Thousands of third-party web interfaces for it are reachable online; an exposed Hermes interface is an exposed agent, not an attack console, so it is not tracked here. |
| [hexstrike-redteam](https://offensive.agency/agent/hexstrike-redteam) | It runs the HexStrike AI server: an exposed instance is listed under HexStrike AI. Existing [hexstrike-ai.yaml](../tags/hexstrike-ai.yaml) covers its reused server; do not duplicate it. |
| [incalmo](https://offensive.agency/agent/incalmo) | A web interface and a local command server on port 8888, for test ranges; none was seen online in November 2026. |
| [kaligpt](https://offensive.agency/agent/kaligpt) | A terminal assistant; nothing is served on the network. |
| [lazyown](https://offensive.agency/agent/lazyown) | The command-and-control dashboard is meant to be reachable; none was seen online in November 2026. |
| [mapta](https://offensive.agency/agent/mapta) | Nothing: the tool has no service and no port. |
| [mcp-for-security](https://offensive.agency/agent/mcp-for-security) | MCP servers started by the assistant; nothing is served on the network. |
| [mcp-kali-server](https://offensive.agency/agent/mcp-kali-server) | Its command API listens on 127.0.0.1:5000 by default. |
| [mitsu](https://offensive.agency/agent/mitsu) | A terminal client; nothing is served on the network. |
| [nebula](https://offensive.agency/agent/nebula) | Careful by default: the core listens on the loopback address and asks for a bearer token; remote access needs explicit options. |
| [numasec](https://offensive.agency/agent/numasec) | A terminal tool; its local server is started on demand only. |
| [openhack](https://offensive.agency/agent/openhack) | A dashboard bound to 127.0.0.1:6969. The "OpenHack Simulator" pages seen online are another product. |
| [pentest-agent-suite](https://offensive.agency/agent/pentest-agent-suite) | Nothing is served on the network. |
| [pentest-ai-agents](https://offensive.agency/agent/pentest-ai-agents) | Nothing to expose: it is a set of Markdown files. |
| [pentest-ai](https://offensive.agency/agent/pentest-ai) | Its API and dashboard listen on 127.0.0.1:8888 by default; no instance was found online. |
| [pentest-copilot](https://offensive.agency/agent/pentest-copilot) | Every port is bound to the loopback address by the compose files. The pages seen online belong to the vendor's hosted edition, not to this open-source version. |
| [pentest-harness](https://offensive.agency/agent/pentest-harness) | Its web interface is local; no instance was found online. |
| [pentestagent](https://offensive.agency/agent/pentestagent) | A terminal application. Its optional MCP server answers with nothing a passive scan can recognise. |
| [pentestcode](https://offensive.agency/agent/pentestcode) | A terminal tool; its inherited local server shows no page of its own online, and its favicons are those of OpenCode. |
| [pentesterflow](https://offensive.agency/agent/pentesterflow) | Nothing is served on the network; its browser capture server binds to the loopback address. |
| [pentestgpt](https://offensive.agency/agent/pentestgpt) | No network service by default. |
| [raptor](https://offensive.agency/agent/raptor) | No console and no service: it works on source code and binaries on the user's machine. |
| [redai](https://offensive.agency/agent/redai) | A terminal tool; nothing is served on the network. |
| [sage-mythic](https://offensive.agency/agent/sage-mythic) | No interface of its own: it installs into a Mythic server. |
| [shannon](https://offensive.agency/agent/shannon) | Nothing is published on the network: no web interface of its own, no API. Its workflow engine stays on the loopback address. |
| [vibe-pentest](https://offensive.agency/agent/vibe-pentest) | A skill for coding agents; nothing is served on the network. |
| [vigilo](https://offensive.agency/agent/vigilo) | Its console title is just "Vigilo", shared with unrelated products, so a passive scan cannot single it out. |
| [virga](https://offensive.agency/agent/virga) | A web interface titled "Virga C2 - Web UI"; none was seen online in November 2026. |
| [vulnbot](https://offensive.agency/agent/vulnbot) | Its only services are a document base API and a Streamlit page taken from another project: they carry no fingerprint of their own. |
| [zen-ai-pentest](https://offensive.agency/agent/zen-ai-pentest) | No console of its own was found online. |
| [zerosecurity](https://offensive.agency/agent/zerosecurity) | It works on a repository from a workstation or a CI job; nothing is served by default. |
