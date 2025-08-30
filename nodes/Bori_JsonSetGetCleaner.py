import os
import json
from pathlib import Path
from .Bori_JsonUtils import gather_files

class Bori_JsonSetGetCleaner:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_folder": ("STRING", {
                    "default": "C:/comfyADMDLoraTrain/ComfyUI/custom_nodes/ComfyUI-Bori-JsonSetGetCleaner/convert"
                }),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "convert_folder"
    OUTPUT_NODE = True
    CATEGORY = "Bori_JsonSetGetCleaner"

    def convert_folder(self, json_folder):
        files = gather_files(json_folder)

        for json_path in files:
            with open(json_path, encoding="utf8") as f:
                data = json.load(f)

            nodes = data.get("nodes", [])
            links = data.get("links", [])

            # Maps for quick lookup
            id_to_node = {n["id"]: n for n in nodes}
            id_to_link = {l[0]: l for l in links}

            # Collect Set/Get nodes
            set_nodes = {}
            get_nodes = []
            for node in nodes:
                if node["type"] == "SetNode":
                    varname = node["widgets_values"][0]
                    set_nodes[varname] = node
                elif node["type"] == "GetNode":
                    get_nodes.append(node)

            # Rewire each GetNode from its SetNode's input
            for get_node in get_nodes:
                varname = get_node["widgets_values"][0]
                set_node = set_nodes.get(varname)
                if not set_node:
                    continue

                # Incoming link to SetNode
                if not set_node.get("inputs"):
                    continue
                input_link_id = set_node["inputs"][0].get("link")
                if input_link_id is None:
                    continue
                input_link = id_to_link.get(input_link_id)
                if not input_link:
                    continue

                # Source of the SetNode input
                src_node_id, src_slot = input_link[1], input_link[2]

                # Redirect GetNode outputs
                for out in get_node.get("outputs", []):
                    for link_id in out.get("links", []):
                        if link_id in id_to_link:
                            link = id_to_link[link_id]
                            link[1] = src_node_id
                            link[2] = src_slot

            # Delete Set/Get nodes
            deleted_ids = {n["id"] for n in nodes if n["type"] in ("SetNode", "GetNode")}
            keep_nodes = [n for n in nodes if n["id"] not in deleted_ids]
            data["nodes"] = keep_nodes

            # Remove dangling links
            new_links = []
            for link in links:
                if len(link) >= 4:
                    src_node = link[1]
                    dest_node = link[3]
                    if src_node in deleted_ids or dest_node in deleted_ids:
                        continue
                new_links.append(link)
            data["links"] = new_links

            # Save JSON
            with open(json_path, "w", encoding="utf8") as f:
                json.dump(data, f, indent=4)

        return {}
