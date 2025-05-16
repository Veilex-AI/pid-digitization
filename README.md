### Overview
This is a repository for managing the workflow of digitizing piping and instrumentation diagrams. Its primary function is to take an image and convert it into a XML graph data structure in machine readable format.

#### How to execute the code.
- prefered version of python is **3.12.8**
- create a virtual environment: **python3 -m venv env**
- activate the virtual environment: **.\env\Scripts\activate**
- install all the packages from requirements.txt into the environment: **pip install -r requirements.txt**

alternatively you could you also create a docker container to run the fast api service for testing the graph creation service.

The source code of this repo is broken down into multiple folders.
- **models**: provides class based attributes for other services to work on.
- **enums**: basic key value pairs for conditional checking, and giving types/status definitions.
- **services**: provides main logical functionalities as features, such as data conversion, symbol prediction, graph creation
- **utils**: provides basic functions that are reused throughout different part of services.

##### If you want to know on how to train the PID dataset for symbol detection please refer to the notion link below. 
https://www.notion.so/Thesis-Extracting-Semantic-Relationship-from-visual-diagrams-14c2e0d11f918084b3b7c3d5f4b58c93 

<br>

#### Feature provided by the project
- **Data Conversion**: Converts the image with annotated data into a python readable format. 
- **Symbol Prediction**: Predicts the symbol bounding boxes in the image using YOLO object detection model. The model is trained using YOLOv8. A already trained path is provided via the configuration to predict the results.
- **Line Detection**: Uses Hough Transformation, a computer vision techniuqe, to detect lines on the pid image.
- **Displaying Image**: Responsible for displaying bounding boxes images and graph based images using matplot lib library.
- **Graph Construction**: A Graph management class that uses techniques to create graph and removes all redundiences in the graph structure.
- **Crop Image**: Crops the image with desired dimensions. ability to filter and adjusts the annotations vertcies that are within the provided dimensions of the image. Moreover, can save the crop result back to its upload path.  
- **Word Prediction**: Predicts the word bounding boxes in the image by using azure document inteligence. A key and endpoint is required for this service to work.


#### Purpose of the config/env file
The configuration file consists of imperative key-value pairs that need to be assigned for the source-code features to work succesfully.
The config file consists of the following key-value pairs.

- **MODEL_PATH**: The path of YOLO object detection model, responsible for identifying symbols in an PID image
- **UPLOAD_PATH**: The path where selected files/images can be uploaded.
- **DATASET_PATH**: The path where the entire dataset exist, which can be used for prediction and can be used for other testing purposes.
- **IMAGE_DIR_NAME**: name of the folder, consisting of images, which is inside "DATASET_PATH"
- **ANNOTATION_DIR_NAME**: name of the annotation folder, consisting of annotations, which is inside "DATASET_PATH"
- **DB_NAME**: a database that is used to store the pid documetns and the xml result of the graph construction.
- **MONGO_URI**: An uri for connection to the database.
- **PID_UPLOAD_PATH**: A path where documents are uploaded.
- **AZURE_DI_ENDPOINT**: azure document inteligence endpoint required for OCR detection.
- **AZURE_DI_KEY**: A key associated with the provided endpoint for OCR detection.

#### Other files
Some other files have been designed to test the service features either independently or in combination to validate their successfull working.

- **cropped_dataset**: Uses data conversion service and crop image service to crop a larger image into smaller images with desired dimensions provided by the user.
- **graph_construction**: test graph construction service test graph functions to check if the provided result can be converted into a minimilistic graph with fewest redundencies.
- **line_detection_test**: checks if line segments are being detect from the pid image. 


#### Future Tasks
- Features to be built around FastAPI which will make testing easier.✅
- Implement the functionality of downloading yolo model from google drive. usage of credentials and token is required to achive this task. ✅
- Merge the verticle or horizontal lines that are intersecting with each other. ✅

<br>

The repo is primarily designed around a "piping and instrumentation diagram" dataset that is taken from the following link
https://drive.google.com/drive/u/0/folders/1gMm_YKBZtXB3qUKUpI-LF1HE_MgzwfeR