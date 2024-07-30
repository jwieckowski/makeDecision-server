# REST API server for Multi-Criteria Decision Analysis calculation

Representational State Transfer (REST) Application Programming Interface (API) for Multi-Criteria Decision Analysis calculations.

Server dedicated for the calculations performed with the Graphical User Interface (GUI) implemented in React. It allows for performing multi-criteria calculations based on the determined structure of connections between MCDA techniques and input data.

The server can be used without the developed GUI and can be adopted to own purposes.

The Flask-RestX package is used as the core of the server functionalities assuring communication and validation.

The `pymcdm` and `pyfdm` packages are used for the multi-criteria calculations.

### Technologies

- Backend
  - Python-Flask-RestX
  - pymcdm
  - pyfdm

### STRUCTURE

```
├── server
│   ├── calculations
│   ├── db
│   ├── examples
│   ├── graphs
│   ├── methods
│   ├── models
│   ├── parsers
│   ├── public
│   ├── routes
│   ├── tests
│   ├── utils
│   ├── wrappers
│   ├── config.py
│   ├── helpers.py
│   ├── server.py
├── .gitignore
├── API.rest
└── LICENSE
└── pyproject.toml
└── README.md
└── requirements.txt
└── setup.txt
```

### Get started

[GUI application](https://make-decision.it)

[Server documentation](https://api.make-decision.it/api/v1/documentation)

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

- Build a Wheel distribution

`python setup.py bdist_wheel`

- Install package locally

`pip install dist/mdserver-{package-version}-py3-none-any.whl`

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
