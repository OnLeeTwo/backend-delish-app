from services.upload import UploadService
from flask import Blueprint, request

import os
from datetime import datetime

# This routes is an example on how to do upload on R2
#
# You can copy and paste this routes to your own routes and integrate the data to the database table for usage.
#

upload_routes = Blueprint("upload_routes", __name__)
R2_DOMAINS = os.getenv("R2_DOMAINS")
upload_service = UploadService()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "mp4"}  # Extension limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # File size limit


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_routes.route("/upload", methods=["PUT"])
def upload_file():
    file = request.files["media"]
    if file.filename == "":
        return {"error": "No selected file"}, 400
    if file and allowed_file(file.filename):
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length > MAX_FILE_SIZE:
            return {"error": "File size exceeds limit"}, 413

        filename = file.filename
        ext_name = os.path.splitext(filename)[1]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"MEDIA-{timestamp}{ext_name}"

        try:
            file_url = upload_service.upload_file(file, new_filename)
            return {"success": "upload success", "file_url": file_url}, 201
        except Exception as e:
            return {"error": str(e)}, 500
    else:
        return {"error": "file type not allowed"}, 415
