# From Eyes To Ears

An early usage of deep learning to to translate image detection into sound using deep learnning and practical engineering.

For this solution we demonstrate the power of pixel level classification by utilizing a pre-trained model and custom trained model to detect image items and represent the picture with sound.
For the pre-trained model we will utilize the MS COCO trained detectron2 panoptic segmentation model.  Then for our custom trained model we will use a standard mask R-CNN Model with our custom classes.
Finally we will query for matching sounds using the sound bible query engine (http://soundbible.com/).

## Contents
From_Eyes_to_Ears.ipynb - training and prediction workbook ("the app")
mask_training_data.ipynb - prepares training, validation and test datasets using the Google Open Images dataset in a format to be read by the main app (MS COCO format) (https://opensource.google/projects/open-images-dataset)
sound_maker.py - sound query/blender library
blended_predictor.py - generates a new predictor given the supplied base panoptic and custom mask r-cnn models

## How to use
 *  use mask_training_data.ipynb to create a training, validation, and test dataset.
   * code is tested to run on google colab
   * GPU Acceleration is not needed for this notebook
   * the first few cells (that define the phase and the files to download) should be adjusted/skipped based on the dataset being generated
   * the final cell of the workbook should only be run once (when all datasets are complete to zip up the final data and upload to to GDrive 
     * You will be prompted to authorize colab access to your GDrive
 * use From_Eyes_to_Ears.ipynb to trian and test the final model and sound generation
   * Use the Chrome browser (safari is not fully supported)
   * code is tested to run on google colab
   * Ensure that the notebook is running in a GPU enabled environment
   * You will need to download the data generated above from your GDrive to the new notebook environment
   * Run all cells until you get to "Prediction Time" (if you run the next cell early it will fail)
   * From here on you will run the next cells as many times as you want to "test"
     * You will then get prompted to uplaod a test image for classification
     * Run all cells to the end of the notebook and you will see the custom classification, default panoptic classification, blended classification and final generated audio

## Limitations of the approach
This approach works best if your custom dataset does not contain classes similar to existing MS COCO classes (http://cocodataset.org/#explore) or you retrain the affected classes.  
So for example guitars and saxaphones seem to work pretty well, but tanks not as much (as they are to "similar" to a car and need a car class to be trained along with them to distinguish them)

## Citations
 * Sound Bible for audio clip query (http://soundbible.com)
 * Google Open Image Dataset for trianing and validation images (https://opensource.google/projects/open-images-dataset) [CC-by 4.0](LICENSE)
 * Common Objects in Context for base classes and pre-trained model and validation (via Detectron2) (http://cocodataset.org/#home) [CC-by 4.0](LICENSE)
 * Detectron2 is Facebook AI Research's deep learning platform for object recognition released under the [Apache 2.0 license](LICENSE).
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
