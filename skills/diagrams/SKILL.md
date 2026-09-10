---
name: diagrams
description: Render architecture and flow diagrams to PNG and SVG with the Python `diagrams` library. Use when the user wants a cloud, infrastructure, or Kubernetes architecture drawn, or a flowchart, C4, or code-structure diagram as an image.
---

# Diagrams

A diagram here is diagram as code: a Python script whose nodes are icon classes from the `diagrams` package and whose edges are Python operators. Graphviz does the layout. You write the script, render it, look at the image, and fix the script until the image reads right.

## 1. Check Graphviz

```bash
command -v dot
```

`diagrams` renders by calling Graphviz's `dot`. If the command prints nothing, tell the user to install Graphviz (`sudo apt install graphviz`, `brew install graphviz`) and wait. It needs root, so it is theirs to run.

The Python side needs no install. Every run goes through `uv run --with diagrams python ...`. Without `uv`, install `diagrams` into a virtualenv with `pip`.

## 2. Ask where it goes

Ask the user for a directory and a base name. The script and both images land there side by side: `<dir>/<name>.py`, `<dir>/<name>.png`, `<dir>/<name>.svg`. With the script beside the images, the next change is an edit and a re-render.

## 3. Discover the nodes

Every component the user named needs a node. Discover each import in the installed package. Class names change between releases, and an import written from memory fails at render time.

Each argument matches, case-insensitively, anywhere in `diagrams.<provider>.<category>.<Name>`. A service name finds its class, a module path lists the whole module:

```bash
uv run --with diagrams python - kafka redis onprem.monitoring <<'EOF'
import sys, pkgutil, importlib, diagrams
terms = [t.lower() for t in sys.argv[1:]]
for m in pkgutil.walk_packages(diagrams.__path__, "diagrams."):
    mod = importlib.import_module(m.name)
    for name, obj in vars(mod).items():
        path = f"{mod.__name__}.{name}".lower()
        if callable(obj) and getattr(obj, "__module__", None) == mod.__name__ \
                and not name.startswith("_") and any(t in path for t in terms):
            print(f"from {mod.__name__} import {name}")
EOF
```

Where things live, since a keyword search only helps once you know the vendor's word for it:

- Cloud providers each have a package: `aws`, `gcp`, `azure`, `k8s`, `oci`, `ibm`, `alibabacloud`, `digitalocean`, `openstack`.
- `onprem` holds self-hosted software: databases, queues, caches, monitoring, CI, proxies.
- `saas` holds hosted products (alerting, chat, CDN, identity).
- `programming` holds `flowchart` shapes (`StartEnd`, `Action`, `Decision`, `InputOutput`) and icons for languages, frameworks, and runtimes. Use it for code structure and control flow.
- `generic` holds vendor-neutral shapes, the fallback when nothing names the product.
- `c4` holds C4 model elements (see the API below).

Two names printing for one icon (`ELB`, `ElasticLoadBalancing`) are aliases of the same class. Pick either.

When nothing fits, use `Custom("label", "<path to png>")` from `diagrams.custom` with an icon file on disk. Download a remote icon first with `urllib.request.urlretrieve`. When the user wants to pick an icon by eye, point them at `https://diagrams.mingrammer.com/docs/nodes/<provider>`.

## 4. Write the script

```python
from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.queue import Kafka
# ... one import per discovered node

with Diagram(
    "Title shown on the image",
    filename=str(Path(__file__).with_suffix("")),
    outformat=["png", "svg"],
    show=False,
    direction="LR",
):
    ...
```

Keep `filename` and `show` exactly as above. `filename` takes no extension and resolves against the working directory, so deriving it from `__file__` writes the images beside the script from wherever it runs. `show=True`, the library default, opens an image viewer.

### API

| Write | Draws |
| :--- | :--- |
| `EC2("web")` | one node; `\n` in the label breaks lines |
| `a >> b`, `a << b`, `a - b` | edge to `b`, edge to `a`, edge with no arrow |
| `a >> b >> c` | a chain |
| `a >> [b, c]`, `[b, c] >> d` | fan-out, fan-in |
| `a >> Edge(label="writes", color="firebrick", style="dashed") >> b` | a styled edge; `style` is `dashed`, `dotted`, or `bold` |
| `with Cluster("VPC"):` | a box around every node created inside it; clusters nest |

A node variable is one box on the image. Reusing the variable reuses the box. Calling the class again draws a second one.

`Diagram` options:

- `direction`: `"LR"` for request flows and pipelines, `"TB"` for hierarchies and flowcharts. `Cluster` takes its own `direction` too.
- `curvestyle`: `"ortho"` (default) or `"curved"`. Graphviz misplaces edge labels on `ortho` edges, so any diagram with labelled edges gets `"curved"`.
- `graph_attr`, `node_attr`, `edge_attr`: dicts of raw Graphviz attributes, string values. The useful ones: `{"pad": "0.5", "nodesep": "0.8", "ranksep": "1.2", "fontsize": "20", "bgcolor": "transparent"}`.

C4 elements are functions in `diagrams.c4`: `Person(name, description)`, `System(name, description, external=False)`, `Container(name, technology, description)`, `Database(name, technology, description)`. Group them with `with SystemBoundary("name"):` as you would a `Cluster`, and label edges with `Relationship("label")` in place of `Edge`.

A list on both sides, `[a, b] >> [c, d]`, raises `TypeError`. Loop over one side:

```python
for src in [a, b]:
    src >> [c, d]
```

## 5. Render and look

```bash
uv run --with diagrams python <dir>/<name>.py
```

Open `<dir>/<name>.png` with your image-reading tool and look at it. It passes when:

- every component the user named is a node, and every relationship they named is an edge pointing the way data or control flows;
- every label reads at the rendered size, and no label sits on top of another label, edge, or icon;
- nodes the user grouped together share a cluster.

A failing image is a script fix and a re-render. Reach for the layout levers in this order: flip `direction`, regroup with `Cluster`, reorder node creation (Graphviz places nodes of a rank in creation order), then widen `nodesep` and `ranksep`.

Done when the PNG passes and the SVG exists beside it. Give the user all three paths.
