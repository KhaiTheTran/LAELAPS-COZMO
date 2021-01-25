# Laelaps

### Team Members
- Saketh Nimmagadda
- Khai Tran
- Lingyue Zhang

### Getting Started
1. Set up virtual env (recommended)

2. `pip install requirements.txt`

3. Set up [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection) 


### Usage
Connect Cozmo and run `python main.py`

### Training Object Detection Model
To retrain our object detection model, first, you need to add more annotated images in `<path_to_cse481c-project>/src/perception/object_detection_tensorflow/data`
The tool we used to label images is [labelImg!](https://github.com/tzutalin/labelImg).
 
The run `python xml_to_csv.py` to generate csv for dataset, and `python generate_tfrecord.py` to process data into
tensorflow format. 

To train model using new data, run
```
python <path to object_detection>/model_main.py --logtostderr --model_dir=<path_to_cse481c-project>/cse481c-project/src/perception/object_detection_predefined/training --pipeline_config_path=<path_to_cse481c-project>/src/perception/object_detection_predefined/training/ssd_mobilenet_v1_coco.config
```

We can generate inference graph by running 
```
python <path to object_detection>/export_inference_graph.py --input_type image_tensor --pipeline_config_path <path_to_cse481c-project>/src/perception/object_detection_predefined/training/ssd_mobilenet_v1_coco.config --trained_checkpoint_prefix <path_to_cse481c-project>/src/perception/object_detection_predefined/training/model.ckpt-<model_check_point_number> --output_directory <path_to_cse481c-project>/src/perception/object_detection_predefined/inference_graph
```

