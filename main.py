import PIL.Image as pl
from mathutils import *
from tqdm import tqdm

image_width = 400
image_height = 400



class Ray:
    def __init__(self):
        self.origin = Vector3(0, 0, 0)
        self.direction = Vector3(1, 0, 0)

class Sphere:
    def __init__(self, center:Vector3, radius:float):
        self.center = center
        self.radius = radius


class World:
    def __init__(self):
        self.objects = [
            Sphere(Vector3(0, 0, 0), 0.5), 
            Sphere(Vector3(0, 0.5, -0.5), 0.25), 
            Sphere(Vector3(0, 0, 500.5), 500)]
        self.lights = [(Vector3(2, 0, -2), 1)]
        self.camera_pos = Vector3(-3, 0, 0.1)
        self.camera_direction = ~Vector3(3, 0, -0.1)
        self.camera_size = (1, 1)

    

    def compute_ray(self, ray:Ray, detect_point:bool=False, detect_normal:bool=False):
        """
        Compute the intersection of a ray with the objects in the world.
        Returns a dictionary with the intersection point and the index of the object in 
          the world.objects list
        
        :param ray: The ray to compute the intersection with.
        :param detect_point: If True, the intersection point will be returned.
        :param detect_normal: If True, the normal at the intersection point will be returned.
        :return: A dictionary with the intersection point and the index of the object in the 
          world.objects list, or None if there is no intersection.
        """
        nearest_point = (Vector3(INF, INF, INF), -1)
        for _object in self.objects:
            t = ray.origin - _object.center # OA - OC = OA + CO = CA = -AC
            
            a = 1 # normalisé
            b = 2 * (t @ ray.direction) # T . u = -AC . u
            c = t.norm() **2 - _object.radius ** 2
            delta = b**2 - (4 * c)
            if delta >= 0:
                x = (- b - delta**0.5) / 2
                if x < 0: x = (- b + delta**0.5) / 2
                if x < 0: return None
                ai = ray.direction * x # AI = tu
                if ai.norm() < nearest_point[0].norm():
                    nearest_point = (ai, self.objects.index(_object))
        if nearest_point[0].norm() < INF: #RENDER_DISTANCE est INF pour l'instant
            i = ray.origin + nearest_point[0] # OI = OA + AI = OA + tu
            return {POINT: i, OBJECT: nearest_point[1]}
        else: return None


world = World()
image = pl.new("RGBA", (image_width, image_height), (0, 0, 0))

print(f"image_size: ({image_width},{image_height}), SSAA: no, output: PNG \n")
for i in tqdm(range(image_height)):
    for j in range(image_width):
        ray = Ray()
        ray.origin.x = world.camera_pos.x
        ray.origin.y = world.camera_pos.y
        ray.origin.z = world.camera_pos.z
        ray.direction = world.camera_direction
        ray.origin.y += 2 * j / (image_width - 1) - 1
        ray.origin.z += 2 * i / (image_height - 1) - 1
        collide_point = world.compute_ray(ray)
        
        
        if collide_point is not None:
            normal  = ~(collide_point[POINT] - world.objects[collide_point[OBJECT]].center) # CI = CO + OI = OI - OC
            shadow_ray = Ray()
            shadow_ray.direction = ~(world.lights[0][0] - collide_point[POINT])
            shadow_ray.origin = collide_point[POINT] + shadow_ray.direction * 0.001
            collide_shadow = world.compute_ray(shadow_ray)
            if collide_shadow is not None:
                color = (0, 0, 0, 255)
            else:
                light_direction = ~(world.lights[0][0] - world.objects[collide_point[1]].center)
                light_intensity = light_direction @ normal
                color = (0, int(255 + light_intensity * 200), 0, 255)
        else:
            color = (0, 0, 0, 255)
        image.putpixel((j, i), color)


ray_count = image_height * image_width
if ray_count < 1000:
    print(f"\n{ray_count} rays processed")
elif ray_count < 1000000:
    print(f"\n{round(ray_count / 1000, 2)}K rays processed")
else:
    print(f"\n{round(ray_count / 1000000, 2)}M rays processed")
image.show()
