<img src="./images/main_logo.png" width="500px" height="100px" title="Github_Logo"/>

# pacemaker-iot-project
This is an implementation of the IoT project for the Social Innovation Competency Course at Yonsei University. You can control the iot device and manage personal records through the streamlit app. See details about the project in [this link](https://drive.google.com/file/d/1UJKlaXSgd2S3Rjg5QQUNvJuLqocD1PlH/view?usp=sharing)

You can visit our [pacemaker streamlit app](https://yuna-102-pacemaker-iot-project-app-dev-xw5z5g.streamlitapp.com/)

<img src="https://i.postimg.cc/mrttxjcL/2022-07-17-2-36-22.png" width="800px" height="500px" title="Github_Logo"/>

## Getting Started
This dev branch is a version for streamlit cloud deployment. Therefore, we do not install pymodi library that can actually control the pacemaker. If you need a version using pymodi, refer to the [modi branch](https://github.com/yuna-102/pacemaker-iot-project/tree/modi)

### Installing
Clone repository
```bash
# clone git repositoty
git clone -b modi https://github.com/yuna-102/pacemaker-iot-project.git 

cd pacemaker-iot-project
```

With conda
```bash
# create conda environment
conda create -n pacemaker python=3.8

# or yon can create environment with conda env file
conda env create -n pacemaker --file environment.yaml

# activate conda environment
conda activate pacemaker
```

Install packages
```bash
pip install -r requirements.txt
```

You can also build an environment by using [Dockerfile](./Dockerfile) 


## Usage

Explain how to run the automated tests for this system

### Running the app
```
streamlit run app.py
```

### Running the pacemaker
```
python pacemaker.py
```

## Built With
* [streamlit](https://docs.streamlit.io/) - The web application framework used


## Contacts
jungyoonchoi22@gmail.com
