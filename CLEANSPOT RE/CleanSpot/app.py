import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from predict import predict_waste

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "cleanspot"

UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

mysql = MySQL(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/checker", methods=["GET", "POST"])
def checker():
    result = None
    if request.method == "POST":
        item = request.form.get("item", "").strip()

        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT item_name, category, disposal_method FROM waste_items "
            "WHERE item_name LIKE %s LIMIT 10",
            (f"%{item}%",)
        )
        result = cursor.fetchall()
        cursor.close()

    return render_template("checker.html", result=result)


@app.route("/guide")
def guide():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT item_name, category, disposal_method FROM waste_items "
        "ORDER BY category, item_name"
    )
    wastes = cursor.fetchall()
    cursor.close()
    return render_template("guide.html", wastes=wastes)


@app.route("/scan")
def scan():
    return render_template("scan.html")


@app.route("/predict", methods=["POST"])
def predict():
    image = request.files.get("image")

    if not image or image.filename == "":
        flash("Please choose an image.", "warning")
        return redirect(url_for("scan"))

    allowed = {"jpg", "jpeg", "png"}
    extension = image.filename.rsplit(".", 1)[-1].lower()
    if extension not in allowed:
        flash("Please upload a JPG, JPEG, or PNG image.", "warning")
        return redirect(url_for("scan"))

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(image_path)

    try:
        category, confidence = predict_waste(image_path)
    except Exception as error:
        flash(f"Prediction error: {error}", "danger")
        return redirect(url_for("scan"))

    return render_template(
        "scan_result.html",
        prediction=category,
        confidence=round(confidence * 100, 2),
        image=filename
    )


@app.route("/report", methods=["GET", "POST"])
def report_waste():
    if request.method == "POST":
        waste_type = request.form.get("waste_type", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()
        image = request.files.get("image")

        if not waste_type or not location:
            flash("Waste type and location are required.", "warning")
            return redirect(url_for("report_waste"))

        filename = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO waste_reports
               (waste_type, location, description, image)
               VALUES (%s, %s, %s, %s)""",
            (waste_type, location, description, filename)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Report submitted successfully.", "success")
        return redirect(url_for("report_waste"))

    return render_template("report.html")


@app.route("/admin/reports")
def admin_reports():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT id, waste_type, location, description,
                  image, report_date, status
           FROM waste_reports
           ORDER BY report_date DESC"""
    )
    reports = cursor.fetchall()
    cursor.close()
    return render_template("admin_reports.html", reports=reports)


@app.route("/admin/stats")
def admin_stats():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM waste_reports")
    total_reports = cursor.fetchone()[0]

    cursor.execute(
        """SELECT waste_type, COUNT(*) AS total
           FROM waste_reports
           GROUP BY waste_type
           ORDER BY total DESC"""
    )
    waste_stats = cursor.fetchall()

    cursor.execute(
        """SELECT location, COUNT(*) AS total
           FROM waste_reports
           GROUP BY location
           ORDER BY total DESC"""
    )
    location_stats = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin_stats.html",
        total_reports=total_reports,
        waste_stats=waste_stats,
        location_stats=location_stats
    )


if __name__ == "__main__":
    app.run(debug=True)
