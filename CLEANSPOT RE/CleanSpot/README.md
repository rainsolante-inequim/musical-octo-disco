# CleanSpot

CleanSpot is a Flask + MySQL web prototype for waste segregation awareness.

## Features

- Waste Checker
- Waste Guide
- Image-based waste classification
- OpenCV image preprocessing
- TensorFlow/Keras ML model
- Improper waste reporting
- Environmental report database
- Admin report statistics

## 1. Install

Use `py -m pip` on Windows if `pip` is not recognized:

```powershell
py -m pip install -r requirements.txt
```

If pip is missing:

```powershell
py -m ensurepip --upgrade
```

## 2. Database

Start MySQL/WAMP, then import `database.sql` into MySQL/phpMyAdmin.

The default configuration in `app.py` is:

- host: localhost
- user: root
- password: empty
- database: cleanspot

Change these if your MySQL setup is different.

## 3. Dataset

Create:

dataset/
  biodegradable/
  recyclable/
  residual/
  special/

Put training images into the matching folders.

Then train:

```powershell
py train_model.py
```

This creates:

model/cleanspot_model.keras
model/classes.txt

## 4. Run

```powershell
py app.py
```

Open the local address shown by Flask in your browser.

## Important

The ML model is only as good as its training data. Test it with separate images that were not used during training, and report the actual results in your technical documentation.
