import torch, torchvision
import detectron2

from detectron2.engine import DefaultPredictor
from detectron2.data import MetadataCatalog
from detectron2.data.catalog import Metadata

class BlendPredictor:
    shrink_threshold = .15

    def __init__(self, panoptic_config, mask_config, panoptic_predictor=None, mask_predictor=None, panoptic_metadata=None, mask_metadata=None, shrink_threshold=None):
        self.po_predictor = panoptic_predictor if panoptic_predictor is not None else DefaultPredictor(panoptic_config)
        self.mask_predictor = mask_predictor if mask_predictor is not None else DefaultPredictor(mask_config)
        self.po_md = panoptic_metadata if panoptic_metadata is not None else MetadataCatalog.get(panoptic_config.DATASETS.TRAIN[0])
        self.mask_md = mask_metadata if mask_metadata is not None else MetadataCatalog.get(mask_config.DATASETS.TRAIN[0])
        self.shrink_threshold = shrink_threshold if shrink_threshold is not None else self.shrink_threshold
        self._merge_metadata()
    
    def _merge_metadata(self):
        added_classes = self.mask_md.get('thing_classes')
        total_classes = self.po_md.get('thing_classes').copy()

        self.offset = len(total_classes)

        for c in added_classes:
            if c not in total_classes:
                total_classes.append(c)
            else:
                total_classes.append(f"custom_{c}")

        self.blend_md = Metadata(thing_classes=total_classes, stuff_classes=po_md.get("stuff_classes"))

    def predict(self, img):
        # First lets run the predictions
        self.panoptic_seg, self.panoptic_seg_info = self.po_predictor(img)["panoptic_seg"] 
        self.mask_output = self.mask_predictor(img)
        return blend_segs(self.panoptic_seg, self.mask_output)

    def blend_segs(self, panoptic_seg, mask_output):
        blend_seg = panoptic_seg.to("cpu").numpy().copy()
        max_seg = blend_seg.max()
        blend_info = segments_info.copy()

        masks = mask_outputs["instances"].to("cpu").get("pred_masks").numpy()
        scores = mask_outputs["instances"].to("cpu").get("scores").numpy()
        classes = mask_outputs["instances"].to("cpu").get("pred_classes").numpy()

        # basic blending
        new_seg_info = []
        instance_ids = {}
        for i in range(len(classes)):
            iid = max_seg + i + 1
            c = classes[i]
            m = masks[i]
            s = scores[i]

            if c in instance_ids:
                instance_ids[c] += 1
            else:
                instance_ids[c] = 0

            blend_seg = blend_seg * ((m - 1) * -1)
            blend_seg = blend_seg + (m * iid)
            area = np.count_nonzero(blend_seg == iid)

            info = {"id": iid, "isthing": True, "score": s, "category_id": c + offset, "instance_id": instance_ids[c], "area": area}
            blend_info.append(info)

        # Remove "dead" instances where the instance has lost more than N% of volume
        final_info = []
        for i in range(len(blend_info)):
            seg = blend_info[i]
            if i >= len(segments_info):
                final_info.append(seg)
                continue
            orig_seg = segments_info[i]
            iid = seg["id"]
            orig_area = orig_seg["area"]
            new_area = np.count_nonzero(blend_seg==iid)
            pct = new_area/orig_area
            if pct > self.shrink_threshold:
                seg["area"] = new_area
                final_info.append(seg)
            else:
                print(f"REMOVING ID: {iid}, Category: {total_classes[seg['category_id']]}, Orig Area: {orig_area}, New Area: {new_area}, PCT: {pct}")
                blend_seg = np.where(blend_seg == iid, 0, blend_seg)

        final_seg = torch.tensor(blend_seg)

        return final_seg, blend_info

