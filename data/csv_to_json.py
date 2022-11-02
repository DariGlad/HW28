import csv
import json

ADS = "ad"
CATEGORIES = "category"
LOCATIONS = "location"
USER = "user"


def csv_to_json(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding="utf-8") as csvf:
        for row in csv.DictReader(csvf):
            to_add = {
                "model": model,
                "pk": int(row["id"] if "id" in row else row["Id"])
            }
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(row[key])
                if value.lower() == "true":
                    row[key] = True
                if value.lower() == "false":
                    row[key] = False
            if "id" in row:
                del row["id"]
            else:
                del row["Id"]

            if "location_id" in row:
                row["location"] = [row["location_id"]]
                del row["location_id"]

            to_add["fields"] = row
            result.append(to_add)

    with open(json_file, "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(result, indent=4, ensure_ascii=False))


csv_to_json(f"{ADS}.csv", f"{ADS}.json", "ads.ad")
csv_to_json(f"{CATEGORIES}.csv", f"{CATEGORIES}.json", "ads.category")
csv_to_json(f"{USER}.csv", f"{USER}.json", "users.user")
csv_to_json(f"{LOCATIONS}.csv", f"{LOCATIONS}.json", "users.location")
