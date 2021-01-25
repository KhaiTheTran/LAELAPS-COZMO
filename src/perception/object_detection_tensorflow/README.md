Resource: https://towardsdatascience.com/creating-your-own-object-detector-ad69dda69c85

Requirement: tensorflow 1.5.0

Set up tensorflow: https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html 

Activate virtualenv:
```
source env/bin/activate
```

Train model:
```
python /Users/starry/TensorFlow/models/research/object_detection/model_main.py --logtostderr --model_dir=/Users/starry/Desktop/CSE481C/cse481c-project/src/perception/object_detection_predefined/training --pipeline_config_path=/Users/starry/Desktop/CSE481C/cse481c-project/src/perception/object_detection_predefined/training/ssd_mobilenet_v1_coco.config
```

Export inference graph:
```
python /Users/starry/TensorFlow/models/research/object_detection/export_inference_graph.py --input_type image_tensor --pipeline_config_path /Users/starry/Desktop/CSE481C/cse481c-project/src/perception/object_detection_predefined/training/ssd_mobilenet_v1_coco.config --trained_checkpoint_prefix /Users/starry/Desktop/CSE481C/cse481c-project/src/perception/object_detection_predefined/training/model.ckpt-200 --output_directory /Users/starry/Desktop/CSE481C/cse481c-project/src/perception/object_detection_predefined/inference_graph
```
