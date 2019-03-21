from maxfw.core import MetadataAPI


class ModelLabelsAPI(MetadataAPI):
    def get(self):
        """Return the labels associated with the model"""

        labels = ['background', 'car', 'motorbike', 'aeroplane', 'cat', 'person', 'bicycle', 'chair', 'pottedplant',
                  'bird', 'cow', 'sheep', 'boat', 'diningtable', 'sofa', 'bottle', 'dog', 'train', 'bus', 'horse', 'tv']

        return labels
