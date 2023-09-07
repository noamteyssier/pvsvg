# pvsvg

## Introduction

a python wrapper of the [`vis.js`](https://visjs.github.io/vis-network/docs/network/)
network visualization library with an additional ability to export static SVG.

Inspired by the excellent python library [`pyvis`](https://pyvis.readthedocs.io/en/latest/tutorial.html)
but I required a function to export the resulting network as a static SVG.

The code for exporting the SVG is taken from [`justinharrell/vis-svg`](https://github.com/justinharrell/vis-svg).

## Installation

You can install this via pip:

``` bash
pip install pvsvg
```

## Usage

This library exposes a single class ( `Network` ) which takes as input
a [networkx `Graph`](https://networkx.org/documentation/stable/reference/classes/graph.html).

All the configuration for node and edge level attributes (like color, size, mass)
are passed transparently to `vis.js` so you can configure your resulting network
via the attributes of your networkx nodes and edges respectively.

You can see
[node level configuration](https://visjs.github.io/vis-network/docs/network/nodes.html)
and
[edge level configuration](https://visjs.github.io/vis-network/docs/network/edges.html)
on the `vis.js` documentation.

### Exporting as SVG

The resulting HTML file will have some configuration buttons built-in.
One of these is the `export-svg` button which will generate the static
SVG and write it to a file (`network.svg`)

Keep in mind that it will write the SVG of whatever is within the `Canvas`
element at the time.
Essentially the view you have within the boundaries of the `Canvas` is exactly
what will be written to the SVG.

> **Note:** Currently the node borders are not being written to the SVG. Besides
> that everything else should appear.

### Example

``` python3
from pvsvg import Network
import networkx as nx

# generate some random graph
g = nx.fast_gnp_random_graph(15, 0.2)

# set node level attributes
for n in g.nodes(data=True):
    id = n[0]
    if id % 2 == 0:
        n[1]["color"] = "red"
    else:
        n[1]["color"] = "blue"

    if id % 3 == 0:
        n[1]["shape"] = "square"
    else:
        n[1]["shape"] = "dot"

    n[1]["label"] = f"Node {id}"
    n[1]["title"] = f"Node {id} has color {n[1]['color']} and shape {n[1]['shape']}"
    n[1]["size"] = (id + 1)

# set edge level attributes
for e in g.edges(data=True):
    e[2]["color"] = {
        "color": "black",
        "inherit": False,
    }

# Instantiate the network
n = Network(g, width=1200)

# Draw the network as an html
n.draw("test.html")
```
