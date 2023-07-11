import base64
import json

from os.path import join
from app.config import PROJECTS, PASSWORD, LOGIN
from app import app, request, jsonify


def save_icon_api(icon_json, dir="img"):
    img_path = join(dir, icon_json["filename"])

    with open(join(app.static_folder, img_path), "wb") as fw:
        bytes_data_image = base64.b64decode(icon_json["data"])
        fw.write(bytes_data_image)

    icon_path = img_path
    return icon_path


@app.route("/api/admin/project", methods=["GET", "POST", "DELETE", "PATCH"])
def manage_projects():
    if request.json["login"] == LOGIN and request.json["password"] == PASSWORD:
        project = {}
        isSucces = False

        if request.method != "POST":
            if not request.json.get("project_id") and request.json.get("project_id") != 0:
                return "Error: Project ID not specified "
            else:
                project_id = request.json["project_id"]
        
        if request.method != "DELETE" and request.method != "GET":
            if not request.json.get("project"):
                return "Error: Project not specified "
            else:
                project = request.json["project"]


        if request.method == "POST":
            project["id"] = len(PROJECTS)
            if project.get("icon"):
                project["icon"] = save_icon_api(project["icon"])
            PROJECTS.append(project)
            isSucces = True
        elif request.method == "PATCH":
            PROJECT = None
            for _project in PROJECTS:
                if _project["id"] == project_id:
                    PROJECT = _project.copy()
            
            if PROJECT == None:
                return 'Project Not Found'
            
            PROJECTS.remove(PROJECT)

            for key in project.keys():
                if key == "icon":
                    PROJECT[key] = save_icon_api(project[key])
                else:
                    PROJECT[key] = project[key]

            project = PROJECT.copy()

            PROJECTS.append(PROJECT)
            isSucces = True
        elif request.method == "DELETE":
            PROJECT = None
            for _project in PROJECTS:
                if _project["id"] == project_id:
                    PROJECT = _project.copy()
            
            if PROJECT == None:
                return 'Project Not Found'
        
            PROJECTS.remove(PROJECT)
            project = PROJECT.copy()
            isSucces = True
        else:
            for _project in PROJECTS:
                if _project["id"] == project_id:
                    project = _project.copy()

            if not project:
                return "Project Not Found"

        if request.method != "GET":
            if isSucces:
                with open("projects.json", "w") as fw:
                    json.dump(PROJECTS, fw)
            else:
                return "Error"
        
        return jsonify(project)
    
    return "Login incorrect"