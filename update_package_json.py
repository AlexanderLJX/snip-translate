import json

with open("package.json", "r") as f:
    package_data = json.load(f)

package_data["type"] = "module"

with open("package.json", "w") as f:
    json.dump(package_data, f, indent=2)
