# REST API server for Multi-Criteria Decision Analysis calculation

Representational State Transfer (REST) Application Programming Interface (API) for Multi-Criteria Decision Analysis calculations.
Server dedicated for the calculations performed with the Graphical User Interface (GUI) implemented in React. It allows for performing multi-criteria calculations based on the determined structure of connections between MCDA techniques and input data.
The server can be used without the developed GUI and can be adopted to own purposes.
The Flask-RestX package is used as the core of the server functionalities assuring communication and validation.
The `pymcdm` and `pyfdm` packages are used for the multi-criteria calculations.

# Communication

- GET /api/v1/descriptions/methods
  - returns descriptions of multi-criteria methods available in the GUI
- GET /api/v2/dictionary/all-methods
  - return dictionaries based on which the data regarding the given techniques is used in the development of the structural decision models in the web application
- POST /api/v1/matrix
  - allows for updating the decision matrix and criteria types from file with verifying the data format, and convert it to list format, then returns it back to web application
- POST /api/v1/results
  - allows for establishing the structure of developed decision model based on which the multi-criteria calculations are performed

### Technologies

- Backend
  - Python-Flask-RestX
  - pymcdm
  - pyfdm

### STRUCTURE

```
├── server
│   ├── examples
│   │   ├── files
│   ├── public
│   │   ├── descriptions
│   │   ├── dictionary
│   │   ├── errors
│   ├── utilities
│   │   ├── Interfaces
│   │   |   ├── __init__.py
│   │   |   ├── additional.py
│   │   |   ├── correlations.py
│   │   |   ├── preferences.py
│   │   |   ├── ranking.py
│   │   |   ├── weights.py
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   ├── files.py
│   │   ├── interface.py
│   │   ├── validator.py
│   ├── server.py
├── .gitignore
├── API.rest
└── requirements.txt
```

### Get started

[GUI application](http://make-decision.it)

[Server documentation](http://api.make-decision.it/api/v1/documentation)

### Run server locally

To run the REST API server locally:

- Clone the repository with the REST API server

```
git clone https://github.com/jwieckowski/makeDecision-server.git
```

- Enter the repository and install dependencies

```
cd makeDecision-server
pip install -r requirements.txt
```

- Run the server

```
cd server
python server.py
```

### Run server tests

- To test the server functionalities

```
cd server
python -m pytest .
```
