from flask import Flask, redirect, jsonify, request, render_template, url_for
from lib import Vector, Window, Sphere, Scene, Light, Material, Wall

app = Flask(__name__)

actual_scene = None

@app.route("/", methods = ["GET", "POST"])
def index():

    if request.method == "POST":

        if not request.form:

            return render_template("index.html", error="Submit a valid form!")

        scene_objects = []
        scene_lights = []

        window_width = request.form.get("width")
        
        if not window_width.isdigit():

            return render_template("index.html", error="Window width must be a valid integer.")
        
        window_width = int(window_width)

        window_height = request.form.get("height")

        if not window_height.isdigit():

            return render_template("index.html", error="Window height must be a valid integer.")
        
        window_height = int(window_height)

        sky_color = request.form.get("sky_color")
        sky_color = is_valid_tuple(sky_color, True)
        
        if not sky_color:

            return render_template("index.html", error="Enter the background color in a valid (R, G, B) format.")
        
        camera_position = request.form.get("camera_position")
        camera_position = is_valid_tuple(camera_position)

        if not camera_position:

            return render_template("index.html", error="Enter a valid 3D position for camera in the format (x, y, z).")

        amount_of_spheres = request.form.get("amount_of_spheres")

        try:

            amount_of_spheres = int(amount_of_spheres)

            if amount_of_spheres < 0:

                return render_template("index.html", error="Amount of spheres cannot be negative.")
        
        except:

            return render_template("index.html", error="Amount of spheres must be a valid integer.")

        centers = request.form.getlist("sphere_center[]")
        radii = request.form.getlist("sphere_radius[]")
        sphere_colors = request.form.getlist("sphere_color[]")
        sphere_reflectivities = request.form.getlist("sphere_reflectivity[]")
        sphere_specular_constants = request.form.getlist("sphere_specular_constant[]")

        for i in range(amount_of_spheres):

            try:

                radius = float(radii[i])
                reflectivity = float(sphere_reflectivities[i])
                specular = float(sphere_specular_constants[i])

                if not (radius > 0 and 0 <= reflectivity <= 1 and specular >= 0):

                    return render_template("index.html", error="Enter valid values for all spheres' radii, reflectivities and specular shading constants.")

                center = is_valid_tuple(centers[i])
                color = is_valid_tuple(sphere_colors[i], True)

                if not (center and color):

                    return render_template("index.html", error="Enter the center positions and colors of the spheres in their valid format.")

                scene_objects.append(Sphere(center, radius, color, Material(reflectivity, specular)))
            
            except:

                return render_template("index.html", error="Radius, reflectivity and specular shading constants must be in the form of integer or float.")

        amount_of_walls = request.form.get("amount_of_walls")

        try:

            amount_of_walls = int(amount_of_walls)

            if amount_of_walls < 0:

                return render_template("index.html", error="Amount of walls cannot be negative.")
        
        except:

            return render_template("index.html", error="Amount of walls must be a valid integer.")

        left_uppers = request.form.getlist("left_upper_corner[]")
        left_lowers = request.form.getlist("left_lower_corner[]")
        right_uppers = request.form.getlist("right_upper_corner[]")
        right_lowers = request.form.getlist("right_lower_corner[]")
        wall_colors = request.form.getlist("wall_color[]")
        wall_reflectivities = request.form.get("wall_reflectivity[]")
        wall_specular_constant = request.form.get("wall_specular_constant[]")

        for i in range(amount_of_walls):

            try:

                reflectivity = float(wall_reflectivities[i])
                specular = float(wall_specular_constant)

                left_upper = is_valid_tuple(left_uppers[i])
                left_lower = is_valid_tuple(left_lowers[i])
                right_upper = is_valid_tuple(right_uppers[i])
                right_lower = is_valid_tuple(right_lowers[i])
                color = is_valid_tuple(wall_colors[i], True)
                

                if not (left_upper and left_lower and right_upper and right_lower and color):
                    print(left_uppers[i])
                    print(left_lowers[i])
                    print(right_uppers[i])
                    print(right_lowers[i])
                    print(wall_colors[i])
                    return render_template("index.html", error="Enter the corner positions and colors of the walls in their right format.")

                scene_objects.append(Wall(left_upper, left_lower, right_upper, right_lower, color, Material(reflectivity, specular)))
            
            except:

                return render_template("index.html", error="Reflectivities and specular shading constants can either be in integer or float.")
        
        amount_of_lights = request.form.get("amount_of_lights")

        try:

            amount_of_lights = int(amount_of_lights)

            if amount_of_lights < 1:

                return render_template("index.html", error="At least one light must exist in the scene.")
        
        except:

            return render_template("index.html", error="Amount of lights can only be in valid integer format.")

        positions = request.form.getlist("light_position[]")
        light_colors = request.form.getlist("light_color[]")

        for i in range(amount_of_lights):

            position = is_valid_tuple(positions[i])
            color = is_valid_tuple(light_colors[i], True)

            if not (color and position):

                return render_template("index.html", error="Enter light colors and light positions in their right formats.")

            scene_lights.append(Light(position, color))
        
        try:

            actual_scene = Scene(Window(window_width, window_height, "image", sky_color), scene_objects, camera_position, scene_lights, 8)
            actual_scene.blit_image()
            render_template("index.html", render_start=True)
            actual_scene = None


        except:

            return render_template("index.html", error="An unexpected error occured while rendering the scene, please check your parameters.")

    return render_template("index.html")

app.route("/progress")
def progress():

    global actual_scene
    if actual_scene:

        return jsonify({"progress": actual_scene.progress})
    
    return jsonify({"progress": 0})

def is_valid_tuple(tuple_string: str, is_color = None):

    if (tuple_string[0] == "(" and tuple_string[-1] == ")" and tuple_string.count(", ") == 2):

        try:

            tuple_string = tuple_string[1:len(tuple_string) - 1]
            elements = tuple_string.split(", ")
            elements = [float(element) for element in elements]

            if is_color:

                for element in elements:

                    if not 0 <= element <= 255:

                        return None
    
            return Vector(elements[0], elements[1], elements[2])
        
        except:

            return None
    
    return None


if __name__ == "__main__":
    app.run(debug=True)
        