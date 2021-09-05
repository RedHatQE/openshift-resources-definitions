import shlex
import subprocess
import json


def resources_dict_from_api_resources():
    resources_dict = {}
    api_resources = subprocess.check_output(
        shlex.split("oc api-resources --no-headers")
    )
    api_resources = api_resources.decode("utf-8")
    for line in api_resources.splitlines():
        line_list = line.split()
        try:
            _, _, api_version, namespaced, kind = line_list
        except ValueError:
            _, api_version, namespaced, kind = line_list

        split_api_version = api_version.split("/")
        api_group = split_api_version[0] if len(split_api_version) > 1 else None
        resources_dict.setdefault(kind, {}).update({"namespaced": namespaced})
        resources_dict.setdefault(kind, {}).update({"api_version": api_version})
        resources_dict[kind].setdefault("api_group", []).append(api_group)

    return resources_dict


if __name__ == "__main__":
    with open("resources_definitions.json", "w") as fd:
        fd.write(json.dumps(resources_dict_from_api_resources()))
