# Syncify 🎵
Ever wonder how compatible your music taste really is with someone else's? Syncify tells you.
Syncify is a Python-based web application that uses the Spotify API to analyze your listening history and compare it to another user's, generating a "music compatibility" score for both your top artists and top tracks.

# Features
***Secure Spotify Login:***
Uses the official Spotify OAuth 2.0 flow to securely authenticate users.

***Top Music Analysis:***
Fetches your top 5 artists and top 5 tracks from the last six months.

***Compatibility Score:***
Calculates a similarity percentage for both artists and tracks using the Jaccard index.

***Clean Web Interface:*** 
A simple and intuitive frontend built with Flask and HTML to display the results.

# How It Works
Syncify's backend is built with the Flask web framework. When a user visits the site:

- They are prompted to log in with their Spotify account. Flask handles the OAuth 2.0 redirect and callback to get an access token from the Spotify API.
- Once authenticated, the app makes API calls to the /me/top/artists and /me/top/tracks endpoints.
- The user's top artists and tracks are stored in Python sets.
- The app calculates the *Jaccard Similarity Coefficient* between the user's sets and a pre-defined "comparison" user's sets. The formula is:
***Similarity = (Size of Intersection) / (Size of Union)***

The resulting scores, along with the user's data, are sent to the frontend as a JSON object and displayed on the page.

# Getting Started

## Prerequisites
- Python 3.x
- A Spotify Developer account and an App created to get your credentials.

## Installation & Configuration
- Clone the repo
- git clone https://github.com/Aidan3141/Syncify.git
- cd Syncify

## Install Python packages

- pip install -r requirements.txt

## Usage
Run the Flask application from your terminal:

python app.py

Open your browser and go to http://127.0.0.1:5000 to see it in action!
