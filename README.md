#Practice Project building Social_Media
# S_Media - Personal Project


## Overview

S_Media is a social media web application developed with Django. This is a personal project built by me to have a better understanding of full-stack application development using Django and some frontend tools.  It allows users to connect, share posts, like and comment on them, and more.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [User Registration](#user-registration)
  - [Posting](#posting)
  - [Interactions](#interactions)
- [Contributing](#contributing)
- [Contact](#contact)

## Features

- User registration and authentication
- User profiles with profile pictures
- Create and share posts
- Like and comment on posts
- Reply to comments
- Get Notifications
- Messages

## Getting Started

Follow these instructions to set up and run the S_Media app on your local machine.

### Prerequisites(Are listed on requirements.txt file) 

- Python (version x.x.x)
- Django (version x.x.x)
- crispy_forms
- crispy_bootstrap5
- allauth

### Installation

1. Clone the repository: `git clone https://github.com/yourusername/s_media.git`
2. Change to the project directory: `cd s_media`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Apply database migrations: `python manage.py migrate
