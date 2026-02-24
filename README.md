# Learning analytics dashboard for conceptual modeling education

This repository contains the code for the learning analytics dashboards for conceptual modeling education. The dashboards are presented in the paper below:
- Tiukhova, E., Verbruggen, C., De Laet, T., Baesens, B., & Snoeck, M. (2025, June). Learning Analytics Dashboard with Peer Comparison for Student Feedback in Conceptual Modeling Education. In International Conference on Business Process Modeling, Development and Support (pp. 301-317). Cham: Springer Nature Switzerland.

## Repository Structure

```
LAD_conceptual_modeling/
├── LICENSE
├── README.md
├── LADs/
│   ├── data/
│   │   ├── Data.xlsx
│   │   ├── Login-passwords.xlsx
│   │   └── hashes.json
│   ├── default/
│   │   ├── assets/
│   │   ├── connection.py
│   │   ├── login.py
│   │   ├── login_fd.py
│   │   ├── logout.py
│   │   ├── myapp.py
│   │   ├── success_master.py
│   │   └── __pycache__/
│   ├── peer/
│   │   ├── assets/
│   │   ├── connection.py
│   │   ├── login.py
│   │   ├── login_fd.py
│   │   ├── logout.py
│   │   ├── myapp.py
│   │   ├── success_master_peer.py
│   │   └── __pycache__/
│   ├── Procfile
│   ├── requirements.txt
│   ├── runtime.txt
│   ├── ESSchedule.json
│   ├── PublishingScheduleMasteryQuizzes.json
│   ├── QuizTypesAtt.json
│   ├── TooltipsText.json

```

## Installation

Install the required dependencies:

```bash
pip install -r LADs/requirements.txt
```

## Notes

- `Data.xlsx` is an example data file containing synthetic values that mimic real data.
- **Disclaimer**: Some logical discrepancies might arise in the way the synthetic data is generated due to edX grading idiosyncrasies.

## Running the Application

To run the applications, navigate to the respective directories and execute the scripts. The scripts expect relative paths to the data folder.

- **Default LAD version**: 
  ```bash
  cd LADs/default
  python myapp.py
  ```
- **Peer LAD version**: 
  ```bash
  cd LADs/peer
  python myapp.py
  ```
## Frontend login
- The login is possible by using login password pairs from LADs/data/Login-passwords.xlsx. The password is compared with its hash in hashes.json and if it matches, the access to the LAD is granted.
- Normally, `hashes.json` should be stored in a separate database such as Firebase for better security and scalability.
