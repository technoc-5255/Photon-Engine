import PIL.Image as pl
from mathutils import *
from tqdm import tqdm

image_width = 1920
image_height = 1080


class Ray:
    def __init__(self):
        self.origin = Vector3(0, 0, 0)
        self.direction = Vector3(1, 0, 0)


class World:
    def __init__(self):
        self.objects = [(Vector3(0, 0, 0), 0.5), (Vector3(0, 0.5, -0.5), 0.25), (Vector3(0, 0, 500.5), 500)]
        self.lights = [(Vector3(2, -2, -2), 1)]
        self.camera_pos = Vector3(-3, 0, 0)
        self.camera_direction = ~Vector3(3, 0, 0)
        self.camera_size = (1, 1)

    def compute_ray(self, ray:Ray):
        nearest_point = (Vector3(INF, INF, INF), -1)
        for _object in self.objects:
            t = ray.origin - _object[0] # OA - OC = OA + CO = CA = -AC
            
            a = 1 # normalisé
            b = 2 * (t @ ray.direction) # T . u = -AC . u
            c = t.norm() **2 - _object[1] ** 2
            delta = b**2 - (4 * c)
            if delta >= 0:
                x = (- b - delta**0.5) / 2
                ai = ray.direction * x # AI = tu
                if ai.norm() < nearest_point[0].norm():
                    nearest_point = (ai, self.objects.index(_object))
        if nearest_point[0].norm() < INF: #RENDER_DISTANCE
            i = ray.origin + nearest_point[0] # OI = OA + AI = OA + tu
            return (i, nearest_point[1])
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
            normal  = ~(collide_point[0] - world.objects[collide_point[1]][0]) # CI = CO + OI = OI - OC
            shadow_ray = Ray()
            ray.origin.x = colli
            
            light_direction = ~(world.lights[0][0] - world.objects[collide_point[1]][0])
            light_intensity = light_direction @ normal
            color = (0, int(255 + light_intensity * 200), 0, 255)
        else:
            color = (0, 0, 0, 255)
        image.putpixel((j, i), color)

print(f"\n{image_height * image_width // 1000}K rays processed")
image.show()
