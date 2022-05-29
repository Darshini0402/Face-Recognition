# Face-Recognition
Microsoft Engage


Steps to set up the virtual environment and run the web application:

Recommended OS : Windows

1.Install python and add to path (Reference: YouTube Video)

2.Clone the repository : https://github.com/Darshini0402/Face-Recognition.git

3. Install Visual Studio (YouTube Timestamp : 04.38)
3.Create virtual environment named “myvenvpy”  under the folder Face-Recognition\FaceRecognition and install recommended libraries
	pip install virtualenv (to install virtual environment)
	virtualenv myvenvpy    (to create a virtual environment named myvenvpy)

4. Activate environment by navigating to Face-Recognition\FaceRecognition folder and execute the command:  myvenvpy\Scripts\activate (Windows) 

5.To install facial_recognition module : pip3 install face_recognition
If it gives error proceed with the following steps
Clone the face_recognition repository
Create virtual environment and run python setup.py install
If it throws error, execute  pip install cmake
Run python setup.py install again
Reference : YouTube Link and Document Link

6. Install other libraries after activating the environment using: pip install -r requirements.txt

7. Execute pip freeze to check if the necessary libraries are installed. 

8. To run the web application navigate to Face-Recognition\FaceRecognition and execute: python manage.py runserver

YouTube Link : https://www.youtube.com/watch?v=xaDJ5xnc8dc
Document Link : https://face-recognition.readthedocs.io/en/latest/installation.html
Module Installation GitHub Repository Link : https://github.com/ageitgey/face_recognition
