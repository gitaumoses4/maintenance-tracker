# Maintenance Tracker :wrench:
Andela Maintenance Tracker Web Project Challenge 1

![GitHub last commit](https://img.shields.io/github/last-commit/gitaumoses4/maintenance-tracker/develop.svg)
![GitHub top language](https://img.shields.io/github/languages/top/gitaumoses4/maintenance-tracker.svg)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/gitaumoses4/maintenance-tracker.svg)
![GitHub contributors](https://img.shields.io/github/contributors/gitaumoses4/maintenance-tracker.svg)
[![Coverage Status](https://coveralls.io/repos/github/gitaumoses4/maintenance-tracker/badge.svg?branch=develop)](https://coveralls.io/github/gitaumoses4/maintenance-tracker?branch=develop)
[![Build Status](https://travis-ci.org/gitaumoses4/maintenance-tracker.svg?branch=develop)](https://travis-ci.org/gitaumoses4/maintenance-tracker)

![Mock Up](https://image.ibb.co/gmP8vy/Mock_Up.jpg)


# Table of Contents
   * [Maintenance Tracker <g-emoji class="g-emoji" alias="wrench" fallback-src="https://assets-cdn.github.com/images/icons/emoji/unicode/1f527.png">🔧</g-emoji>](#maintenance-tracker-wrench)
      * [UI Template](#ui-template)
      * [Pivotal Tracker Project](#pivotal-tracker-project)
      * [Introduction](#introduction)
         * [Project Overview](#project-overview)
         * [Required Features](#required-features)
         * [Images](#images)
         * [Fonts](#fonts)
         * [Wireframes](#wireframes)
      * [Login page](#login-page)
      * [Signup page](#signup-page)
      * [User Home Page](#user-home-page)
      * [User Create Request Page](#user-create-request-page)
      * [User View Previous Requests](#user-view-previous-requests)
      * [User Track Request Status](#user-track-request-status)
      * [Admin Home Page](#admin-home-page)
      * [Admin Change Request Status](#admin-change-request-status)
      * [Admin can view all requests and filter them.](#admin-can-view-all-requests-and-filter-them)
         * [UI Inspiration](#ui-inspiration)
         
## Installation
To have the API running you will need to create a virtual environment and install the requirements
So navigate to the `/API` directory where the API is located.

### Create a virtual environment
```bash
$ python3 -m venv venv;
$ source venv/bin/activate
```
#### Install requirements
```bash
$ pip install -r requirements.txt
```

## Running the application
After the configuration, you will run the app 
```bash
$ export FLASK_APP=run.py
$ flask run
```
### Endpoints
All endpoints can be now accessed from the following url on your local computer
```
http://localhost:5000/api/v1/
```
Or from Heroku
```
https://maintenance-tracker-api.herokuapp.com/api/v1/
```

### Available endpoints
|  Endpoint  | Task  |
|  ---  | --- |
| `POST api/v1/users/signup` | Users can sign up |
| `POST api/v1/users/login`  | Users can log in |
| `POST api/v1/admin/login` | Admin can login in |
| `DELETE api/v1/admin/logout` | Admin can logout |
| `DELETE api/v1/users/lgout` | Users can logout |
| `POST api/v1/users/requests` | User can create a maintenance request | 
| `GET api/v1/users/requests` | User can get all their requests |
| `PUT api/v1/users/requests/<requestId>` | User can edit a request |
| `GET api/v1/users/requests/<requestId>` | User can get a request details|
| `GET api/v1/admin/requests` | Admin can get all the requests |
| `GET api/v1/admin/requests/<requestId>` | Admin can get a request by id |
| `PUT api/v1/admin/requests/<requestId>` | Admin can edit a request |
| `POST api/v1/admin/requests/<requestId>/feedback` | Admin can create a feedback for request |
| `GET api/v1/users/requests/<requestId>/feedback` | User can get feedback for request |
| `POST api/v1/admin/users/<userId>/notifications` | Admin can send a notification to a user |
| `GET api/v1/users/notifications/<notificationId>` | User can get notification by id |
| `GET api/v1/users/notifications` | User can get all notifications |
| `PUT api/v1/users/notifications/<notificationId>` | Set a notification as read |
| `GET api/v1/users/details` | Get user details |

## UI Template
You can view the UI template on [Github Pages](https://gitaumoses4.github.io/maintenance-tracker)

## Pivotal Tracker Project
You can view the [Pivotal Tracker stories](https://www.pivotaltracker.com/n/projects/2173234)

## Introduction
### Project Overview
Maintenance Tracker App is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.

### Required Features
1. Users can [create an account](https://gitaumoses4.github.io/maintenance-tracker/UI/register.html) and [log in](https://gitaumoses4.github.io/maintenance-tracker/UI/login.html) 
2. Users should be able to [make maintenance or repair requests](https://gitaumoses4.github.io/maintenance-tracker/UI/user/new-request.html).
3. An admin should be able to [approve/reject](https://gitaumoses4.github.io/maintenance-tracker/UI/admin/request.html) a repair/maintenance request.
4. The admin should be able to [mark a request as resolved](https://gitaumoses4.github.io/maintenance-tracker/UI/admin/request.html) once it is done.
5. The admin should be able to [view all maintenance/repair requests](https://gitaumoses4.github.io/maintenance-tracker/UI/admin/requests.html) on the application.
6. The admin should be able to [filter](https://gitaumoses4.github.io/maintenance-tracker/UI/admin/requests.html) requests.
7. A user can [view all](https://gitaumoses4.github.io/maintenance-tracker/UI/user/requests.html) of his/her requests

### Images
The following images are used in this project.
1. [Android Cell Phone](https://www.pexels.com/photo/android-android-phone-cell-phone-cellphone-404280/) by Noah Erickson on [Pexels](https://www.pexels.com)
2. [Laptop](https://www.pexels.com/photo/computer-keyboard-laptop-screen-109371/) by Monoar Rahman on [Pexels](https://pexels.com)
3. [Desktop Wireless Keyboard](https://www.pexels.com/photo/black-desktop-wireless-keyboard-on-the-note-6184/) by Kaboompics.com on [Pexels](https://pexels.com)
4. [Camera](https://www.pexels.com/photo/black-camera-226243/) by Gourav Ahir on [Pexels](https://pexels.com)
5. [Yahama Keyboard Piano](https://www.pexels.com/photo/black-yamaha-piano-164743/) by [Pixabay](https://pixabay.com) on [Pexels](https://pexels.com)
6. [Auomobile Repair](https://www.pexels.com/photo/adult-auto-automobile-automotive-558375/) by Fancycrave on [Pexels](https://pexels.com)

### Fonts
The following font are used for this project.

1. [Dosis](https://fonts.google.com/specimen/Dosis) font by Google Fonts

### Wireframes
Wireframes are created using [MockFlow](http://mockflow.com)

## Login page

Users will provide their login information in order to access the website.

![Login Page](https://image.ibb.co/c8ey88/Login.png)

## Signup page
Users can sign up with their email in order to get an account.
![Sign up Page](https://image.ibb.co/mBimvo/Signup.png)

## User Home Page
The user will be provided with this dashboard when they successfully sign up and log in.

![User Home Page](https://image.ibb.co/kKdmvo/User_Home.png)

## User Create Request Page
The user can create a Maintenance Request and submit it.

![User Create Request](https://image.ibb.co/jKmQsd/user_request.png)

## User View Previous Requests
The user can view their request history.

![User Requests](https://image.ibb.co/geVfo8/user_requests.png)

## User Track Request Status
The user can track the status of their request.
![User Request](https://image.ibb.co/d0waMT/user_create_request.png)

## Admin Home Page
The admin will be provided with this dashboard when they successfully sign up and log in.

![Admin Home Page](https://image.ibb.co/bDREFo/admin_home.png)

## Admin Change Request Status
The admin can view a request and set it as approved or rejected.
![Admin Request](https://image.ibb.co/mP2t88/admin_request.png)

## Admin can view all requests and filter them.
![Admin Requests](https://image.ibb.co/deV8ao/admin_requests.png)

### UI Inspiration

User Interface inspired by [Semantic UI](https://semantic-ui.com)