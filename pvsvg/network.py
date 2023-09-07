import os
import json
from typing import Optional, Union
import networkx as nx
from jinja2 import Template


class Network:
    def __init__(
        self,
        graph: nx.Graph,
        width: Union[int, str] = "100%",
        height: Union[int, str] = "800px",
        bgcolor: str = "#ffffff",
        physics_kwargs: Optional[dict] = None,
    ):
        """
        Initialize a new Network object.

        This will handle all network related operations and generate the
        required html and javascript to display the network.
        """
        self.graph = graph
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self._initialize_paths()
        self._set_physics_kwargs(physics_kwargs)
        self._update_figure_size()

    def _initialize_paths(self):
        """
        initialize paths to templates, styles and scripts
        """
        module_dir = os.path.dirname(__file__)
        self.template_path = os.path.join(module_dir, "templates/template.html")
        self.style_path_slider = os.path.join(module_dir, "styles/slider.css")
        self.style_path_vis = os.path.join(module_dir, "styles/vis-network.min.css")
        self.script_path_vis = os.path.join(module_dir, "scripts/vis.js")
        self.script_path_canvas2svg = os.path.join(module_dir, "scripts/canvas2svg.js")

    def _set_physics_kwargs(self, physics_kwargs: dict):
        self._options_physics = {
            "enabled": True,
            "barnesHut": {
                "theta": 0.5,
                "gravitationalConstant": -2000,
                "centralGravity": 0.3,
                "springLength": 95,
                "springConstant": 0.04,
                "damping": 0.09,
                "avoidOverlap": 0.0,
            },
        }
        if physics_kwargs is not None:
            self._options_physics.update(physics_kwargs)
        self._json_physics = json.dumps(self._options_physics)

    def _update_figure_size(self):
        if isinstance(self.width, int):
            self.width = f"{self.width}px"
        elif isinstance(self.width, float):
            self.width = f"{self.width * 100}%"
        elif isinstance(self.width, str):
            if self.width.endswith("%") or self.width.endswith("px"):
                pass
            else:
                raise ValueError(
                    "width must be either a percentage or a pixel value, e.g. '100%' or '100px'"
                )
        if isinstance(self.height, int):
            self.height = f"{self.height}px"
        elif isinstance(self.height, float):
            self.height = f"{self.height * 100}%"
        elif isinstance(self.height, str):
            if self.height.endswith("%") or self.height.endswith("px"):
                pass
            else:
                raise ValueError(
                    "height must be either a percentage or a pixel value, e.g. '100%' or '100px'"
                )

    def _load_template(self):
        with open(self.template_path, "r") as f:
            self._template_content = f.read()

    def _load_styles(self):
        with open(self.style_path_slider, "r") as f:
            self._style_content_slider = f.read()

        with open(self.style_path_vis, "r") as f:
            self._style_content_vis = f.read()

    def _load_scripts(self):
        with open(self.script_path_vis, "r") as f:
            self._script_content_vis = f.read()

        with open(self.script_path_canvas2svg, "r") as f:
            self._script_content_canvas2svg = f.read()

    def _build_node_json(self):
        self._node_attrs = []
        for n in self.graph.nodes(data=True):
            node_attr = {}
            node_attr["id"] = n[0]
            for k in n[1].keys():
                node_attr[k] = n[1][k]
            self._node_attrs.append(node_attr)

        self._node_json = json.dumps(self._node_attrs)

    def _build_edge_json(self):
        self._edge_attrs = []
        for e in self.graph.edges(data=True):
            edge_attr = {}
            edge_attr["from"] = e[0]
            edge_attr["to"] = e[1]
            for k in e[2].keys():
                edge_attr[k] = e[2][k]
            self._edge_attrs.append(edge_attr)

        self._edge_json = json.dumps(self._edge_attrs)

    def _initialize_html(self, filename: str):
        """
        Initializes the html file.
        """
        self._load_template()
        self._load_styles()
        self._load_scripts()
        self._build_node_json()
        self._build_edge_json()

        template = Template(self._template_content)
        data = {
            "WIDTH": self.width,
            "HEIGHT": self.height,
            "BG_COLOR": self.bgcolor,
            "SLIDER_CSS": self._style_content_slider,
            "VIS_CSS": self._style_content_vis,
            "VIS_JS": self._script_content_vis,
            "CANVAS2SVG_JS": self._script_content_canvas2svg,
            "NODES": self._node_json,
            "EDGES": self._edge_json,
            "OPTIONS_PHYSICS": self._json_physics,
        }
        html = template.render(data)
        with open(filename, "w") as f:
            f.write(html)

    def draw(self, filename: str):
        """
        Draws the network into an html canvas.
        """
        self._initialize_html(filename)
