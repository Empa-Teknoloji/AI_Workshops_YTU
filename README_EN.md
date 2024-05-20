<p align="center"><img src="additionals/university-workshops-ytu-banner-en.png" alt="University Workshops" style="display: block; margin: 0 auto" height=/></p>


## Welcome to University Workshops!

Hello there, 

Welcome to Empa Electronics' first University Workshop event, Yıldız Technical University Workshop!

This landing page will inform you about AI session and guide you to set up everthing you need to join our event & follow activities step-by-step.

By using this page, you will:

- get all custom files and model artifacts to use in workshop.
- install all the prerequisites.
- download (_clone_) this repository.
- install "virtualenv" tool to create a virtual Python environment.
- create & activate your virtual Python environment.
- install all the required packages in your virtual environment.

> **Important Note:** To stay up-to-date, we recommend you to check for possible changes before the workshop:  
```
git pull origin master
```

## Activities in AI Session

We will be having you in _four_ different activities in our AI session. We will define a problem to solve and develop an AI solution to our problem in two different ways. The schedule is here:

| Activity | Approx. Time | Requirements |
| ------ | ------ | ------ | 
| Problem Definition - Human Activity Recognition | 10 min.| - |
| Machine Learning Flashback | 15 min.|  - |
| Bare-Metal ML Solution Development | 25 min.| Python3 & Virtual Environment|
| Alternative way with NanoEdge AI Studio | 25 min.| NanoEdge AI Studio |

## Prerequisites

- Python3 (Preferably 3.9 or 3.10) ([realpython.com/installing-python](https://realpython.com/installing-python))
- Git
- Nano Edge AI Studio ([stm32ai.st.com/download-nanoedgeai/](https://stm32ai.st.com/download-nanoedgeai/))
- Workshop Repository & Python Environment ([See Below](github.com/Empa-Teknoloji/Workshop_YTU#before-we-meet))

Please click the links and follow the installation instructions. 

## Environment Setup

In order to set everything up and join workshop properly, you need to follow (_run in the terminal_) these steps below in your local machine.  

1- Clone the repository:
```
git clone https://github.com/denizcelikai/AI_Workshops_YTU.git
```
2- Install a virtual environment tool:
```
// for Ubuntu
sudo apt install virtualenv

// for Windows
pip3 install virtualenv
```
3- Create & activate your virtual environment:
```
virtualenv WORKSHOP_ENV

// for Ubuntu
source WORKSHOP_ENV/bin/activate

// for Windows 
.\WORKSHOP_ENV\Scripts\activate
```
4- Go to your repository directory & install required packages:

```
cd Workshop_YTU
pip3 install -r requirements.txt
```
_If everything seems okay in your terminal, you're good to go with your environment._ :blush: