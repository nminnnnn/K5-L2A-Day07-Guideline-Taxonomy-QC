"""Chuẩn hóa kq.zip và tách COCO theo assignment.csv để tái lập hồ sơ Day 07."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "submission"
DEFAULT_SOURCE = ROOT.parent / "kq.zip"
CORRECTIONS_PATH = SUBMISSION / "qc" / "source_corrections.json"


def load_assignment() -> dict[str, list[str]]:
    with (SUBMISSION / "qc" / "assignment.csv").open(encoding="utf-8", newline="") as stream:
        return {
            row["image"]: row["annotators"].split("|")
            for row in csv.DictReader(stream)
        }


def load_taxonomy() -> dict:
    return json.loads((SUBMISSION / "taxonomy.json").read_text(encoding="utf-8"))


def load_source(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        candidates = [name for name in archive.namelist() if name.endswith(".json")]
        if len(candidates) != 1:
            raise ValueError(f"Cần đúng một JSON trong {path}; tìm thấy {candidates}")
        return json.loads(archive.read(candidates[0]).decode("utf-8"))


def canonical_name(name: str) -> str:
    return {"tuktuk": "tuk_tuk"}.get(name, name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()

    assignment = load_assignment()
    taxonomy = load_taxonomy()
    source = load_source(args.source.resolve())
    corrections = json.loads(CORRECTIONS_PATH.read_text(encoding="utf-8"))
    removed_ids = set(corrections["remove_annotation_ids"])
    relabel = {int(key): value for key, value in corrections["relabel"].items()}
    allowed = [entry["name"] for entry in taxonomy["classes"]]
    category_by_id = {entry["id"]: canonical_name(entry["name"]) for entry in source["categories"]}
    unknown = sorted(set(category_by_id.values()) - set(allowed))
    if unknown:
        raise ValueError(f"Nguồn có class ngoài taxonomy: {unknown}")

    output_categories = [
        {"id": index, "name": name, "supercategory": ""}
        for index, name in enumerate(allowed, 1)
    ]
    output_category_id = {entry["name"]: entry["id"] for entry in output_categories}
    source_images = {entry["id"]: entry for entry in source["images"]}
    image_id_by_name = {Path(entry["file_name"]).name: entry["id"] for entry in source["images"]}
    if set(image_id_by_name) != set(assignment):
        raise ValueError("Danh sách ảnh trong nguồn không khớp assignment.csv")

    normalized_annotations = []
    clipped = 0
    for annotation in source["annotations"]:
        if int(annotation["id"]) in removed_ids:
            continue
        image = source_images[annotation["image_id"]]
        width, height = float(image["width"]), float(image["height"])
        x, y, box_width, box_height = map(float, annotation["bbox"])
        x2, y2 = x + box_width, y + box_height
        nx1, ny1 = max(0.0, x), max(0.0, y)
        nx2, ny2 = min(width, x2), min(height, y2)
        if (nx1, ny1, nx2, ny2) != (x, y, x2, y2):
            clipped += 1
        if nx1 >= nx2 or ny1 >= ny2:
            raise ValueError(f"Annotation {annotation['id']} không còn bbox hợp lệ sau khi cắt biên")
        class_name = relabel.get(int(annotation["id"]), category_by_id[annotation["category_id"]])
        attrs = annotation.get("attributes") or {}
        normalized = {
            "id": int(annotation["id"]),
            "image_id": int(annotation["image_id"]),
            "category_id": output_category_id[class_name],
            "bbox": [round(nx1, 2), round(ny1, 2), round(nx2 - nx1, 2), round(ny2 - ny1, 2)],
            "area": round((nx2 - nx1) * (ny2 - ny1), 2),
            "iscrowd": int(annotation.get("iscrowd", 0)),
        }
        if class_name != taxonomy["ignore_class"]:
            normalized["attributes"] = {
                "occluded_level": str(attrs.get("occluded_level", "0")),
                "truncated": "yes" if (x <= 0 or y <= 0 or x2 >= width or y2 >= height) else str(attrs.get("truncated", "no")).lower(),
                "can_review": bool(attrs.get("can_review", False)),
            }
        normalized_annotations.append(normalized)

    next_id = max(entry["id"] for entry in normalized_annotations) + 1
    for addition in corrections["add_annotations"]:
        image_id = image_id_by_name[addition["image"]]
        x, y, box_width, box_height = addition["bbox"]
        class_name = addition["category"]
        normalized_annotations.append({
            "id": next_id,
            "image_id": image_id,
            "category_id": output_category_id[class_name],
            "bbox": [x, y, box_width, box_height],
            "area": round(box_width * box_height, 2),
            "iscrowd": 0,
            "attributes": addition["attributes"],
        })
        next_id += 1

    members = sorted({member for codes in assignment.values() for member in codes})
    labels_dir = SUBMISSION / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)
    for member in members:
        names = [name for name, codes in assignment.items() if member in codes]
        source_ids = {image_id_by_name[name] for name in names}
        images = [dict(source_images[image_id]) for image_id in sorted(source_ids)]
        for image in images:
            image["file_name"] = Path(image["file_name"]).name
        annotations = [entry for entry in normalized_annotations if entry["image_id"] in source_ids]
        data = {
            "licenses": source.get("licenses", []),
            "info": source.get("info", {}),
            "categories": output_categories,
            "images": images,
            "annotations": annotations,
        }
        target = labels_dir / f"{member}.json"
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{target.relative_to(ROOT)}: {len(images)} ảnh, {len(annotations)} annotation")
    print(
        f"Chuẩn hóa {len(normalized_annotations)} annotation; cắt {clipped} bbox về biên ảnh; "
        f"loại {len(removed_ids)}, đổi lớp {len(relabel)}, thêm {len(corrections['add_annotations'])}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
