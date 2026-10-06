from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parent
if (ROOT / ".diagram-deps").exists():
    sys.path.insert(0, str(ROOT / ".diagram-deps"))
graphviz_bin = Path(r"C:\Program Files\Graphviz\bin")
if graphviz_bin.exists():
    os.environ["PATH"] = str(graphviz_bin) + os.pathsep + os.environ.get("PATH", "")

from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.device import Mobile
from diagrams.generic.network import Firewall

OUTPUT = ROOT / "img"
OUTPUT.mkdir(parents=True, exist_ok=True)
ICON = ROOT / "icons" / "whatsapp.png"
if not ICON.exists():
    raise FileNotFoundError(f"Falta el icono local: {ICON}")

graph_attr = {
    "fontname": "Arial", "fontsize": "22", "fontcolor": "#16362C",
    "bgcolor": "white", "pad": "0.35", "nodesep": "0.45",
    "ranksep": "0.85", "splines": "spline", "newrank": "true",
    "labelloc": "t", "labeljust": "c", "dpi": "160",
}
node_attr = {"fontname": "Arial", "fontsize": "12", "fontcolor": "#243746"}
edge_attr = {
    "fontname": "Arial", "fontsize": "11", "color": "#64748B",
    "fontcolor": "#475569", "penwidth": "1.5", "arrowsize": "0.8",
}

def cluster_style(fill, border):
    return {"style": "rounded,filled", "bgcolor": fill, "fillcolor": fill, "color": border,
            "fontname": "Arial", "fontsize": "15", "fontcolor": "#243746",
            "margin": "24", "penwidth": "1.2", "labeljust": "l"}

with Diagram(
    "EcoRecicla AQP · Diagrama de despliegue",
    filename=str(OUTPUT / "despliegue"), outformat="png",
    show=False, direction="LR", graph_attr=graph_attr,
    node_attr=node_attr, edge_attr=edge_attr,
) as diagram:
    with Cluster("Clientes", graph_attr=cluster_style("#EFF6FF", "#B5CBE2")) as clients:
        vecinos = Users("Vecinos /\nMunicipalidad")
        reciclador = Mobile("Reciclador")
        with clients.dot.subgraph() as column:
            column.attr(rank="same")
            column.node(vecinos.nodeid)
            column.node(reciclador.nodeid)

    internet = Firewall("Internet\nAcceso seguro")

    with Cluster("VPS · EcoRecicla AQP", graph_attr=cluster_style("#ECFDF5", "#9ACCB4")) as vps:
        aplicacion = Server("PWA + API REST\nMonolito modular")
        base_datos = PostgreSQL("PostgreSQL\nEsquemas por módulo")
        # Una columna dentro del VPS evita estirar horizontalmente el grupo.
        with vps.dot.subgraph() as column:
            column.attr(rank="same")
            column.node(aplicacion.nodeid)
            column.node(base_datos.nodeid)
        aplicacion >> Edge(label="SQL", color="#278260") >> base_datos

    with Cluster("Servicios externos", graph_attr=cluster_style("#F8FAFC", "#CBD5E1")) as services:
        mapas = Server("API de mapas /\nGeolocalización")
        whatsapp = Custom("WhatsApp\nBusiness API", str(ICON))
        with services.dot.subgraph() as column:
            column.attr(rank="same")
            column.node(mapas.nodeid)
            column.node(whatsapp.nodeid)
        mapas >> Edge(style="invis") >> whatsapp

    vecinos >> Edge(label="HTTPS") >> internet
    reciclador >> Edge(label="HTTPS") >> internet
    internet >> Edge(label="HTTPS") >> aplicacion
    aplicacion >> Edge(label="HTTPS") >> mapas
    aplicacion >> Edge(label="HTTPS") >> whatsapp

print(f"Generado: {OUTPUT / 'despliegue.png'}")