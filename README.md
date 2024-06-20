### How to Run the Information Retrieval System

This document provides detailed instructions on how to set up and run the Information Retrieval System. Before starting, ensure you have Python installed on your system. This project is developed using Django, and you can run it directly using a command line interface or through Visual Studio Code with a pre-configured `launch.json`.

#### Requirements:

* Python 3.7 or higher
* Microsoft Word (only required for reading `.doc` files via `pywin32`)

#### Step 1: Clone the Repository

First, clone the repository to your local machine or download the source code from the provided link.

```
https://github.com/ahmadjz/Information-Retrieval-Homework.git
cd Information-Retrieval-Homework
```

#### Step 2: Install Dependencies

Navigate to the project directory where the `requirements.txt` file is located and run the following command to install the required Python libraries.

```
pip install -r requirements.txt
```

#### Step 3: Run the Project

##### Option A: Using Command Line

You can start the server using the Django command line utility. Navigate to the root of the Django project where the `manage.py` file is located and run:

```
python manage.py runserver
```

This will start the development server on `http://127.0.0.1:8000/`, and you should be able to access the web application by navigating to this address in your web browser.

##### Option B: Using Visual Studio Code

If you prefer using Visual Studio Code (VS Code), ensure you have the Python extension installed and configured.

1. Open the project folder in VS Code.
2. Go to the Run view by clicking on the Run icon in the Activity Bar on the side of the window.
3. From the dropdown in the Run view, select the configuration defined in `launch.json` for Django.
4. Click the green play button to start the server.

Visual Studio Code will start the Django server using the configurations specified in `launch.json`, and you will see the output in the terminal window within VS Code.

#### Step 4: Access the Application

Once the server is running, open your preferred web browser and go to `http://127.0.0.1:8000/` to start using the Information Retrieval System.
