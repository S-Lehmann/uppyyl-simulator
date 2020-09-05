# Uppyyl Simulator

A Python implementation of a DBM-based simulator for Uppaal models.

## Getting Started

In this section, you will find instructions to setup and run the Uppyyl Simulator on your local machine.

### Prerequisites

#### Python

Install Python >=3.8 for this project.

#### Virtual Environment

If you want to run the project in a dedicated virtual environment, first install virtualenv:
```
python3.8 -m pip install virtualenv
```

And create a virtual environment:

```
cd project_folder
virtualenv uppyyl-env
```

Then, activate the virtual environment on macOS and Linux via:

```
source ./uppyyl-env/bin/activate
```

or on Windows via:

```
source .\uppyyl-env\Scripts\activate
```

### Installing

To install the Uppyyl Simulator directly from GitHub, run the following command:

```
python3.8 -m pip install -e git://github.com/S-Lehmann/uppyyl-simulator.git#egg=uppyyl-simulator
```

To install the project from a local directory instead, run:

```
python3.8 -m pip install -e path_to_project_root
```

### Usage

The project can both be used as a package for other projects, or as a standalone simulator using the provided CLI tool.

To run the standalone CLI tool, execute the following command:

```
python3.8 -m uppyyl_simulator
```

## Running the tests

To run the tests (and optionally measure coverage), execute either:

```
make run_all_tests
make run_all_coverage
```

## Authors

* **Sascha Lehmann** - *Initial work* - [S-Lehmann](https://github.com/S-Lehmann)

See also the list of [contributors](https://github.com/slehmann/uppyyl-simulator/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* The original Uppaal model checking tool can be found at http://www.uppaal.org/.
* The project is associated with the [Institute for Software Systems](https://www.tuhh.de/sts) at Hamburg University of Technology.
