import argparse
import csv
import sqlite3
import xml.sax.saxutils as xmlutils
from collections import Counter, defaultdict
from pathlib import Path


SYMBOL_KINDS = {"class", "interface", "enum", "method", "function"}
EDGE_KINDS = {"calls", "extends", "implements", "instantiates", "references"}


def package_name(file_path: str, depth: int) -> str:
    parts = Path(file_path).with_suffix("").parts
    if not parts:
        return "(root)"
    return ".".join(parts[: min(depth, len(parts))])


def label_for(row: sqlite3.Row) -> str:
    name = row["qualified_name"] or row["name"] or row["id"]
    if row["kind"] in {"method", "function"} and row["signature"]:
        return f"{name}{row['signature']}"
    return name


def write_nodes_csv(path: Path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Id", "Label", "kind", "file_path", "line", "package"])
        for row in rows:
            writer.writerow(
                [
                    row["id"],
                    label_for(row),
                    row["kind"],
                    row["file_path"],
                    row["start_line"],
                    package_name(row["file_path"], 4),
                ]
            )


def write_edges_csv(path: Path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Source", "Target", "Type", "kind", "weight"])
        for row in rows:
            writer.writerow([row["source"], row["target"], "Directed", row["kind"], 1])


def write_gexf(path: Path, nodes, edges, node_attrs):
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        handle.write('<gexf xmlns="http://www.gexf.net/1.3" version="1.3">\n')
        handle.write('  <graph mode="static" defaultedgetype="directed">\n')
        handle.write('    <attributes class="node">\n')
        handle.write('      <attribute id="kind" title="kind" type="string"/>\n')
        handle.write('      <attribute id="package" title="package" type="string"/>\n')
        handle.write('      <attribute id="file_path" title="file_path" type="string"/>\n')
        handle.write('      <attribute id="line" title="line" type="integer"/>\n')
        handle.write("    </attributes>\n")
        handle.write('    <attributes class="edge">\n')
        handle.write('      <attribute id="kind" title="kind" type="string"/>\n')
        handle.write("    </attributes>\n")
        handle.write("    <nodes>\n")
        for node_id, label, attrs in nodes:
            handle.write(f'      <node id="{xmlutils.escape(node_id)}" label="{xmlutils.escape(label)}">\n')
            handle.write("        <attvalues>\n")
            for key, value in attrs.items():
                handle.write(f'          <attvalue for="{key}" value="{xmlutils.escape(str(value))}"/>\n')
            handle.write("        </attvalues>\n")
            handle.write("      </node>\n")
        handle.write("    </nodes>\n")
        handle.write("    <edges>\n")
        for index, row in enumerate(edges):
            source = xmlutils.escape(row["source"])
            target = xmlutils.escape(row["target"])
            kind = xmlutils.escape(row["kind"])
            handle.write(f'      <edge id="{index}" source="{source}" target="{target}" weight="1">\n')
            handle.write("        <attvalues>\n")
            handle.write(f'          <attvalue for="kind" value="{kind}"/>\n')
            handle.write("        </attvalues>\n")
            handle.write("      </edge>\n")
        handle.write("    </edges>\n")
        handle.write("  </graph>\n")
        handle.write("</gexf>\n")


def export_symbol_graph(conn: sqlite3.Connection, out_dir: Path, limit_nodes: int | None):
    conn.row_factory = sqlite3.Row
    kind_params = ",".join("?" for _ in SYMBOL_KINDS)
    rows = conn.execute(
        f"""
        SELECT *
        FROM nodes
        WHERE kind IN ({kind_params})
        ORDER BY
            CASE kind
                WHEN 'class' THEN 0
                WHEN 'interface' THEN 1
                WHEN 'enum' THEN 2
                WHEN 'method' THEN 3
                ELSE 4
            END,
            qualified_name
        {f'LIMIT {int(limit_nodes)}' if limit_nodes else ''}
        """,
        tuple(sorted(SYMBOL_KINDS)),
    ).fetchall()
    node_ids = {row["id"] for row in rows}
    edge_params = ",".join("?" for _ in EDGE_KINDS)
    edges = conn.execute(
        f"""
        SELECT source, target, kind
        FROM edges
        WHERE kind IN ({edge_params})
        """,
        tuple(sorted(EDGE_KINDS)),
    ).fetchall()
    edges = [row for row in edges if row["source"] in node_ids and row["target"] in node_ids]

    write_nodes_csv(out_dir / "mc-symbol-nodes.csv", rows)
    write_edges_csv(out_dir / "mc-symbol-edges.csv", edges)
    gexf_nodes = [
        (
            row["id"],
            label_for(row),
            {
                "kind": row["kind"],
                "package": package_name(row["file_path"], 4),
                "file_path": row["file_path"],
                "line": row["start_line"],
            },
        )
        for row in rows
    ]
    write_gexf(out_dir / "mc-symbols.gexf", gexf_nodes, edges, {})
    return len(rows), len(edges)


def export_package_graph(conn: sqlite3.Connection, out_dir: Path, depth: int):
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT file_path, kind
        FROM nodes
        WHERE kind IN ('class', 'interface', 'enum')
        """
    ).fetchall()

    packages = Counter(package_name(row["file_path"], depth) for row in rows)
    package_kinds = defaultdict(Counter)
    for row in rows:
        package_kinds[package_name(row["file_path"], depth)][row["kind"]] += 1

    nodes = []
    for package, count in packages.items():
        nodes.append(
            (
                package,
                package,
                {
                    "kind": "package",
                    "package": package,
                    "file_path": "",
                    "line": count,
                },
            )
        )

    edges_counter = Counter()
    edge_rows = conn.execute(
        """
        SELECT e.source, e.target, e.kind, s.file_path AS source_file, t.file_path AS target_file
        FROM edges e
        JOIN nodes s ON s.id = e.source
        JOIN nodes t ON t.id = e.target
        WHERE e.kind IN ('calls', 'extends', 'implements', 'instantiates', 'references')
        """
    ).fetchall()
    for row in edge_rows:
        source_pkg = package_name(row["source_file"], depth)
        target_pkg = package_name(row["target_file"], depth)
        if source_pkg != target_pkg:
            edges_counter[(source_pkg, target_pkg, row["kind"])] += 1

    edges = [
        {"source": source, "target": target, "kind": kind, "weight": weight}
        for (source, target, kind), weight in edges_counter.items()
        if source in packages and target in packages
    ]

    with (out_dir / "mc-package-nodes.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Id", "Label", "kind", "class_count", "interface_count", "enum_count", "total"])
        for package, total in packages.items():
            kinds = package_kinds[package]
            writer.writerow([package, package, "package", kinds["class"], kinds["interface"], kinds["enum"], total])

    with (out_dir / "mc-package-edges.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Source", "Target", "Type", "kind", "weight"])
        for row in edges:
            writer.writerow([row["source"], row["target"], "Directed", row["kind"], row["weight"]])

    write_gexf(out_dir / "mc-packages.gexf", nodes, edges, {})
    return len(nodes), len(edges)


def main():
    parser = argparse.ArgumentParser(description="Export CodeGraph SQLite data for Gephi.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--package-depth", default=4, type=int)
    parser.add_argument("--symbol-limit", default=0, type=int, help="0 means no limit")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(args.db) as conn:
        symbol_counts = export_symbol_graph(conn, args.out, args.symbol_limit or None)
        package_counts = export_package_graph(conn, args.out, args.package_depth)

    print(f"Exported symbol graph: {symbol_counts[0]} nodes, {symbol_counts[1]} edges")
    print(f"Exported package graph: {package_counts[0]} nodes, {package_counts[1]} edges")
    print(f"Output: {args.out}")


if __name__ == "__main__":
    main()
