### **P&ID Use-case**

- How to train a YOLO model with images and annotation.
    - Step by step process of Training a YOLO model for component/symbol detection
        - Create a new environment in python preferably version 3.10.9 or 3.9.0
            - `pip install virtualenv`
            - `python3 -m virtualenv -p python3.10.9 env` (for creating python env)
            - `.\env\Scripts\activate` (to activate the environment)
        - clone this [repo](https://github.com/THU-MIG/yolov10.git). this will be used to train the model on your desired dataset.
        - After cloning, go to the root of the repository, and use the following commands `pip install .` and `pip install -r requirements.txt`. This will install all the packages in the new environment that you created.
        - Load all the weights URL from these links. There is a code provided below that you can use to load them in the weight folder of the repository. One of these weights can be used to per-train the model for your own dataset. Run this scripts under the repo you just cloned.
            
            ```python
            import os
            import urllib.request
            # Create a directory for the weights in the current working directory
            weights_dir = os.path.join(os.getcwd(), "weights")
            os.makedirs(weights_dir, exist_ok=True)
            # URLs of the weight files
            urls = [
            "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10n.pt",
            "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10s.pt",
            "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10m.pt",
            "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10b.pt",
            "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10x.pt",
            "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10l.pt"
            ]
            # Download each file
            for url in urls:
            	file_name = os.path.join(weights_dir, os.path.basename(url))
            	urllib.request.urlretrieve(url, file_name)
            	print(f"Downloaded {file_name}")
            ```
            
        - set the environment variable `PYTORCH_CUDA_ALLOC_CONF` to `expandable_segments:True` . You can do this in the command line on windows or Terminal in linux.
            - on windows set  `set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`
        - Now, before you train the model, you first have to prepare a dataset. The dataset should consist of images and its corresponding annotations. The folder tree should be created in the following tree format for training and validation dataset.
            - \dataset
                - \train
                    - \images
                    - \labels
                - \valid
                    - \images
                    - \labels
        - You will have to add images and labels in the train and valid folders. Here is how you will do it in both cases
            - put all of your training images in the image folder.
            - make sure that the labels are in the labels folder. For each image that has a specific name (with extension), should have a annotation file, in the text format, in the corresponding labels folder. So if the name of the image `0.jpg`, the name of the label should be  `0.jpg.txt` in the labels folder. This way YOLO would be able to detect on where the annotations for the image file are and training would be made possible.
            - the text file in the labels has a specific format that you have to add and it is the following. A class name followed by the normalized bounding box values which are in the order topX, topY, bottomX, bottomY (i.e. top left coordinates, bottom coordinates). They should be displayed in a row by row fashion.
                - for example: `9 0.76 0.79 0.08 0.06`
            - If the the structure of directories and the labels are not provided as described in the previous bullet points, then training the model will not work.
        - in the root of the repository you have to create a yaml file. You can call it anything i.e. config.yaml file and should have the following values defined in the code snipt below.
            
            ```yaml
            train: <YOUR TRAIN PATH HERE>
            val: <YOUR VAL PATH HERE>
            
            nc: <number of classes>
            names: <all names/labels of the classes>
            ```
            
            - The config values should consist of train and validation path. Remember you created your dataset and added that to a particular path of your choice. You have to provide the train and val path in the following train and val keys.
            - The nc would be the number of classes that are provided in training and the names value are there labels in the chronological order.
            - There are plenty of other options you could add to this yaml file. for more information visit https://docs.ultralytics.com/usage/cfg/#export-settings
        - You have now setup everything you need to start performing your training. You must now use a command to start the training of your model. If you do not have a good GPU the training will be slow.
            - The following command should be used in the cmd or terminal to perform this operation. You may change the batch size, epochs and imgsz according to your resources and your own convenience.
            - `yolo task=detect mode=train epochs=10 batch=8 plots=True imgsz=1088 model=./weights/yolov10n.pt data=config.yaml`
            - the epochs or batch size can be changed according to whatever your wish
    - Perform OCR through document intelligence through Microsoft Azure.