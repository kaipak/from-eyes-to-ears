# From Eyes To Ears

An early usage of deep learning to to translate image detection into sound using deep learnning and practical engineering.

For this solution we demonstrate the power of pixel level classification by utilizing a pre-trained model and custom trained model to detect image items and represent the picture with sound.
For the pre-trained model we will utilize the MS COCO trained detectron2 panoptic segmentation model.  Then for our custom trained model we will use a standard mask R-CNN Model with our custom classes.
Finally we will query for matching sounds using the sound bible query engine [http://soundbible.com/].

## Contents
From_Eyes_to_Ears.ipynb - training and prediction workbook ("the app")
mask_training_data.ipynb - prepares training, validation and test datasets using the Google Open Images dataset in a format to be read by the main app (MS COCO format) (https://opensource.google/projects/open-images-dataset)
sound_maker.py - sound query/blender library
blended_predictor.py - generates a new predictor given the supplied base panoptic and custom mask r-cnn models

## Limitations of the approach
This approach works best if your custom dataset does not contain classes similar to existing MS COCO classes (http://cocodataset.org/#explore) or you retrain the affected classes.  
So for example guitars and saxaphones seem to work pretty well, but tanks not as much (as they are to "similar" to a car and need a car class to be trained along with them to distinguish them)

## Citations
Detectron2 is Facebook AI Research's deep learning platform for object recognition
Detectron2 is released under the [Apache 2.0 license](LICENSE).
### Citing Detectron2
If you use Detectron2 in your research or wish to refer to the baseline results published in the [Model Zoo](MODEL_ZOO.md), please use the following BibTeX entry.
```BibTeX
@misc{wu2019detectron2,
  author =       {Yuxin Wu and Alexander Kirillov and Francisco Massa and
                  Wan-Yen Lo and Ross Girshick},
  title =        {Detectron2},
  howpublished = {\url{https://github.com/facebookresearch/detectron2}},
  year =         {2019}
}
```
