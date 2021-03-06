import json
from shapely.geometry import Polygon, MultiPolygon

classes = ["armchair", "lamp", "chair", "wardrobe", "desk",
           "couch", "shelf", "bed", "dining_table"]
class_weights = {'armchair': 0.079456544379896146,
 'bed': 0.028866859166950479,
 'chair': 0.13942879882330855,
 'couch': 0.038575104688560381,
 'desk': 0.083724911259357243,
 'dining_table': 0.059900300391638142,
 'lamp': 0.33833361193911593,
 'shelf': 0.20583138380315716,
 'wardrobe': 0.025882485548015925}
top_level_key = "aabb"


def iou(target_bboxes, predicted_bboxes):
    target_polys = MultiPolygon([Polygon(i) for i in target_bboxes]).buffer(0)
    predicted_polys = MultiPolygon([Polygon(i) for i in predicted_bboxes]).buffer(0)
    intersection = target_polys.intersection(predicted_polys).area
    union = target_polys.union(predicted_polys).area

    try:
        return intersection / union
    except ZeroDivisionError as e:
        return 0


def multiclass_iou(target_result, predicted_result):
    target_result = json.loads(target_result)[top_level_key]
    predicted_result = json.loads(predicted_result)[top_level_key]
    class_ious = {cl: iou(target_result[cl], predicted_result[cl]) for cl in classes}
    weighted_iou = sum([cl_iou * class_weights[cl] for cl, cl_iou in class_ious.items()])
    return weighted_iou
