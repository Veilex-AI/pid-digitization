### Overview
This is a repository for managing the workflow of digitizing piping and instrumentation diagrams. Its primary function is to take an image and convert it into a graph data strcuture which is a machine readable format.

#### How to execute the code.
- prefered version of python is **3.12.8**
- create a virtual environment: **python3 -m venv env**
- activate the virtual environment: **.\env\Scripts\activate**
- install all the packages in the environment: **.\env\Scripts\activate**


The source code of this repo is broken down into multiple folders.
- **models**: provides class based attributes for other services to work on.
- **enums**: basic key value pairs for conditional checking, and giving types/status definitions.
- **services**: provides main logical functionalities as features, such as data conversion, symbol prediction, graph creation
- **utils**: provides basic functions that are reused throughout different part of services.

##### If you want to know on how to train the PID dataset for symbol detection please refer to the notion link below. 
https://www.notion.so/Thesis-Extracting-Semantic-Relationship-from-visual-diagrams-14c2e0d11f918084b3b7c3d5f4b58c93 

<br>

#### Feature provided by the repository
- **Data Conversion**:
- **Symbol Prediction**:
- **Line Detection**:
- **Displaying Image**:
- **Graph Construction**:


#### Purpose of the config file
mention the purpose of the config files here.

#### Other files
mention other files in root here


The repo is primarily designed around a "piping and instrumentation diagram" dataset that is taken from the following link
https://drive.google.com/drive/u/0/folders/1gMm_YKBZtXB3qUKUpI-LF1HE_MgzwfeR