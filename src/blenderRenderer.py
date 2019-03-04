import bpy

import os
import glob
import math
import random
import datetime
import argparse
from easydict import EasyDict as edict



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, default='/home/yunhsuan/Desktop/blender_synthetic', help='root directory')
    # parser.add_argument('')
    args = parser.parse_args()
    return args

def get_cfg():
    __C = edict()

    cfg = __C

    # the camera
    __C.CAMERA = edict()
    __C.CAMERA.RESOLUTION_X = 900
    __C.CAMERA.RESOLUTION_Y = 1200
    __C.CAMERA.PERCENTAGE = 100 # 100

    __C.CAMERA.SAMPLE = 256

    # the camera 1
    __C.CAMERA1 = edict()
    __C.CAMERA1.LOCATION_X = 0
    __C.CAMERA1.LOCATION_Y = 0
    __C.CAMERA1.LOCATION_Z = 13

    __C.CAMERA1.ROTATION_X = math.pi * 0 / 180
    __C.CAMERA1.ROTATION_Y = 0
    __C.CAMERA1.ROTATION_Z = math.pi * 0 / 180


    # the camera 2
    __C.CAMERA2 = edict()
    __C.CAMERA2.LOCATION_X = 0
    __C.CAMERA2.LOCATION_Y = -7
    __C.CAMERA2.LOCATION_Z = 7

    __C.CAMERA2.ROTATION_X = math.pi * 35 / 180
    __C.CAMERA2.ROTATION_Y = 0
    __C.CAMERA2.ROTATION_Z = 0

    # the camera 3
    __C.CAMERA3 = edict()
    __C.CAMERA3.LOCATION_X = -5.5
    __C.CAMERA3.LOCATION_Y = 0
    __C.CAMERA3.LOCATION_Z = 4.5

    __C.CAMERA3.ROTATION_X = math.pi * 40 / 180
    __C.CAMERA3.ROTATION_Y = 0
    __C.CAMERA3.ROTATION_Z = math.pi * -90 / 180

    # the camera 4
    __C.CAMERA4 = edict()
    __C.CAMERA4.LOCATION_X = -4
    __C.CAMERA4.LOCATION_Y = -6
    __C.CAMERA4.LOCATION_Z = 4

    __C.CAMERA4.ROTATION_X = math.pi * 45 / 180
    __C.CAMERA4.ROTATION_Y = 0
    __C.CAMERA4.ROTATION_Z = math.pi * -30 / 180

    # the camera 5
    __C.CAMERA5 = edict()
    __C.CAMERA5.LOCATION_X = 4
    __C.CAMERA5.LOCATION_Y = 6
    __C.CAMERA5.LOCATION_Z = 4

    __C.CAMERA5.ROTATION_X = math.pi * 45 / 180
    __C.CAMERA5.ROTATION_Y = 0
    __C.CAMERA5.ROTATION_Z = math.pi * 150 / 180


    # the image plane
    __C.PLANE = edict()
    __C.PLANE.LOCATION_X = 0
    __C.PLANE.LOCATION_Y = 0
    __C.PLANE.LOCATION_Z = 0

    __C.PLANE.ROTATION_X = 0
    __C.PLANE.ROTATION_Y = 0
    __C.PLANE.ROTATION_Z = 0


    __C.PLANE.DIMENSION_X = 9
    __C.PLANE.DIMENSION_Y = 12
    __C.PLANE.DIMENSION_Z = 1


    # the occluder
    __C.OBJECT = edict()
    __C.OBJECT.LOCATION_X = 0
    __C.OBJECT.LOCATION_Y = 0
    __C.OBJECT.LOCATION_Z = 18

    __C.OBJECT.ROTATION_X = 0
    __C.OBJECT.ROTATION_Y = 0
    __C.OBJECT.ROTATION_Z = 0

    __C.OBJECT.SCALE_X = 1
    __C.OBJECT.SCALE_Y = 3
    __C.OBJECT.SCALE_Z = 0.2

    __C.OBJECT.LOCATION_MIN = -1
    __C.OBJECT.LOCATION_MAX = 1
    __C.OBJECT.LOCATION_Z_MIN = 14
    __C.OBJECT.LOCATION_Z_MAX = 18


    __C.OBJECT.ROTATION_MIN = math.pi * 0 / 180
    __C.OBJECT.ROTATION_MAX = math.pi * 90 / 180


    # the hdri
    __C.HDRI = edict()
    __C.HDRI.STRENGTH_MIN = 0.1
    __C.HDRI.STRENGTH_MAX = 0.3


    # the light source
    __C.LIGHT = edict()
    __C.LIGHT.TYPE = 'SPOT'
    __C.LIGHT.ANGLE = math.pi * 45 / 180
    __C.LIGHT.SHADOW_SOFT_MIN = 0.3 # 0.3 ~ 0.8
    __C.LIGHT.SHADOW_SOFT_MAX = 0.8 # 0.3 ~ 0.8

    __C.LIGHT.STRENGTH_MIN = 3000 # 3000 ~ 20000
    __C.LIGHT.STRENGTH_MAX = 20000 # 3000 ~ 20000


    __C.LIGHT.LOCATION_X = 0
    __C.LIGHT.LOCATION_Y = 0
    __C.LIGHT.LOCATION_Z = 22

    __C.LIGHT.ROTATION_X = 0
    __C.LIGHT.ROTATION_Y = 0 
    __C.LIGHT.ROTATION_Z = 0


    return cfg

class BlenderRenderer(object):
    """docstring for BlenderRenderer"""
    def __init__(self, root_dir, cfg):
        super(BlenderRenderer, self).__init__()
        self.setPath(root_dir)
        self.doc_num = self.getDocNum()
        self.mdl_num = self.getMdlNum()
        self.hdri_num = self.getHdriNum()

        self.cfg = cfg

        print('[ CONFIG ] # documents: {}, # 3d model: {}, # HDRI : {}'.format(self.doc_num, self.mdl_num, self.hdri_num))
        self.initEnv()
        

    def renderAll(self, render_num):
        total_num = self.doc_num * self.mdl_num * self.hdri_num * len(self.cameras) * render_num
        print('[ RENDER ] Total render num = {}'.format(total_num))
        
        nonShadowList = []
        shadowList = []
        # choose 1 document
        # choose 1 3d model
        # choose 1 HDRI
        
        total_cnt, doc_cnt = 0, 0
        print('[ TIMESTAMP ] {}'.format(datetime.datetime.now().strftime('%H:%M:%S')))
        for doc in self.getDocList():
            self.renderSettingDoc(doc)
            hdri_cnt = 0
            for hdri in self.getHdriList():
                self.renderSettingHdri(hdri)
                cam_cnt = 0
                for cam in self.cameras:
                    self.renderSettingCamera(cam)
                    # self.renderSetting(doc, mdl, hdri, cfg)
                    render_cnt = 0
                    for idx in range(render_num):
                        self.addRandomEffect()
                        
                        mdl_cnt = 0
                        for mdl in self.getMdlList():
                            nonShadowImg = os.path.join(self.non_shadow_dir, 'D{}M{}H{}C{:02d}N{:05d}.png'.format(
                                os.path.splitext(doc)[0], os.path.splitext(mdl)[0], os.path.splitext(hdri)[0], cam_cnt+1, render_cnt+1))
                            nonShadowList.append(self.renderNonShadowImg(nonShadowImg))
                            self.renderSettingMdl(mdl)
                            shadowImg = os.path.join(self.shadow_dir, 'D{}M{}H{}C{:02d}N{:05d}.png'.format(
                                os.path.splitext(doc)[0], os.path.splitext(mdl)[0], os.path.splitext(hdri)[0], cam_cnt+1, render_cnt+1))
                            shadowList.append(self.renderShadowImg(shadowImg))
                            self.deleteMdl()
                            print('\t[ Progress ] Total: [ {} / {} ], document: [ {} / {} ], 3D model: [ {} / {} ], HDRI: [ {} / {} ], camera: [ {} / {} ], render: [ {} / {} ]'.format(
                                total_cnt+1, total_num, doc_cnt+1, self.doc_num, mdl_cnt+1, self.mdl_num, hdri_cnt+1, self.hdri_num, cam_cnt+1, len(self.cameras), render_cnt+1, render_num))
                            mdl_cnt += 1
                            total_cnt += 1
                        render_cnt += 1
                    cam_cnt += 1
                hdri_cnt += 1
            doc_cnt += 1
            print('[ TIMESTAMP ] {}'.format(datetime.datetime.now().strftime('%H:%M:%S')))
            
        print('[ RENDER ] Over')
        return nonShadowList, shadowList

    def initEnv(self):
        # delete all default object
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # set cycle render
        bpy.context.scene.render.engine = 'CYCLES'        
        # create camera
        camera_data = bpy.data.cameras.new('Camera')

        camera1 = bpy.data.objects.new('Camera1', camera_data)
        camera1.location = (self.cfg.CAMERA1.LOCATION_X, self.cfg.CAMERA1.LOCATION_Y, self.cfg.CAMERA1.LOCATION_Z)
        camera1.rotation_euler = (self.cfg.CAMERA1.ROTATION_X, self.cfg.CAMERA1.ROTATION_Y, self.cfg.CAMERA1.ROTATION_Z)
        bpy.data.scenes[0].objects.link(camera1)

        camera2 = bpy.data.objects.new('Camera2', camera_data)
        camera2.location = (self.cfg.CAMERA2.LOCATION_X, self.cfg.CAMERA2.LOCATION_Y, self.cfg.CAMERA2.LOCATION_Z)
        camera2.rotation_euler = (self.cfg.CAMERA2.ROTATION_X, self.cfg.CAMERA2.ROTATION_Y, self.cfg.CAMERA2.ROTATION_Z)
        bpy.data.scenes[0].objects.link(camera2)
        
        camera3 = bpy.data.objects.new('Camera3', camera_data)
        camera3.location = (self.cfg.CAMERA3.LOCATION_X, self.cfg.CAMERA3.LOCATION_Y, self.cfg.CAMERA3.LOCATION_Z)
        camera3.rotation_euler = (self.cfg.CAMERA3.ROTATION_X, self.cfg.CAMERA3.ROTATION_Y, self.cfg.CAMERA3.ROTATION_Z)
        bpy.data.scenes[0].objects.link(camera3)
        
        camera4 = bpy.data.objects.new('Camera4', camera_data)
        camera4.location = (self.cfg.CAMERA4.LOCATION_X, self.cfg.CAMERA4.LOCATION_Y, self.cfg.CAMERA4.LOCATION_Z)
        camera4.rotation_euler = (self.cfg.CAMERA4.ROTATION_X, self.cfg.CAMERA4.ROTATION_Y, self.cfg.CAMERA4.ROTATION_Z)
        bpy.data.scenes[0].objects.link(camera4)
        
        camera5 = bpy.data.objects.new('Camera5', camera_data)
        camera5.location = (self.cfg.CAMERA5.LOCATION_X, self.cfg.CAMERA5.LOCATION_Y, self.cfg.CAMERA5.LOCATION_Z)
        camera5.rotation_euler = (self.cfg.CAMERA5.ROTATION_X, self.cfg.CAMERA5.ROTATION_Y, self.cfg.CAMERA5.ROTATION_Z)
        bpy.data.scenes[0].objects.link(camera5)
        
        bpy.data.scenes[0].update()
        self.cameras = [camera1, camera2, camera3, camera4, camera5]
        # init render parameter
        bpy.data.scenes['Scene'].render.resolution_x = self.cfg.CAMERA.RESOLUTION_X
        bpy.data.scenes['Scene'].render.resolution_y = self.cfg.CAMERA.RESOLUTION_Y
        bpy.data.scenes['Scene'].render.resolution_percentage = self.cfg.CAMERA.PERCENTAGE
        bpy.data.scenes['Scene'].cycles.samples = self.cfg.CAMERA.SAMPLE

        # create plane 
        bpy.ops.mesh.primitive_plane_add(
            location=(self.cfg.PLANE.LOCATION_X, self.cfg.PLANE.LOCATION_Y, self.cfg.PLANE.LOCATION_Z),
            rotation=(self.cfg.PLANE.ROTATION_X, self.cfg.PLANE.ROTATION_Y, self.cfg.PLANE.ROTATION_Z)
        )
        bpy.context.object.dimensions = (9, 12, 0)
        
        # add material and texture to the plane
        self.plane = bpy.data.objects['Plane']

        planeMat = bpy.data.materials.new(name='PlaneMaterial')
        planeMat.use_nodes = True
        planeMat.preview_render_type='FLAT'

        planeMatNodes = planeMat.node_tree.nodes

        self.planeTex = planeMatNodes.new(type='ShaderNodeTexImage')
        # planeTex.image = bpy.data.images.load('/home/yunhsuan/Desktop/blender_synthetic/img/0001.png')
        planeMat.node_tree.links.new(planeMatNodes['Diffuse BSDF'].inputs['Color'], self.planeTex.outputs['Color'])
        self.plane.data.materials.append(planeMat)
        self.plane.data.uv_textures.new()

        # create my own object
        # TODO


        # init hdri image as world texture
        world = bpy.data.worlds.new(name='World')
        bpy.context.scene.world = world
        world.use_nodes = True

        self.bg = world.node_tree.nodes['Background']
        self.env = world.node_tree.nodes.new(type='ShaderNodeTexEnvironment')
        world.node_tree.links.new(self.env.outputs['Color'], self.bg.inputs['Color'])
        # create light source
        bpy.ops.object.lamp_add(
            type=self.cfg.LIGHT.TYPE,
            location=(self.cfg.LIGHT.LOCATION_X, self.cfg.LIGHT.LOCATION_Y, self.cfg.LIGHT.LOCATION_Z)
        )
        bpy.context.object.rotation_euler = (self.cfg.LIGHT.ROTATION_X, self.cfg.LIGHT.ROTATION_Y, self.cfg.LIGHT.ROTATION_Z)
        bpy.data.lamps['Spot'].spot_size = self.cfg.LIGHT.ANGLE
        # bpy.data.lamps['Spot'].shadow_soft_size = self.cfg.LIGHT.SHADOW_SOFT
        # light = bpy.data.objects['Spot']
        # light

    def renderSettingDoc(self, doc):
        # set doc image
        self.planeTex.image = bpy.data.images.load(os.path.join(self.doc_dir, doc))
        self.plane.data.uv_textures[0].data[0].image = bpy.data.images.load(os.path.join(self.doc_dir, doc))
        
    def renderSettingMdl(self, mdl):
        imported_obj = bpy.ops.import_scene.obj(filepath=os.path.join(self.mdl_dir, mdl))
        self.obj = bpy.context.selected_objects[0]
        coord_x = random.uniform(self.cfg.OBJECT.LOCATION_MIN, self.cfg.OBJECT.LOCATION_MAX)
        coord_y = random.uniform(self.cfg.OBJECT.LOCATION_MIN, self.cfg.OBJECT.LOCATION_MAX)
        coord_z = random.uniform(self.cfg.OBJECT.LOCATION_Z_MIN, self.cfg.OBJECT.LOCATION_Z_MAX)
        rotate_z = random.uniform(self.cfg.OBJECT.ROTATION_MIN, self.cfg.OBJECT.ROTATION_MAX)
        
        self.obj.location = (coord_x, coord_y, coord_z)
        self.obj.rotation_euler = (self.cfg.OBJECT.ROTATION_X, self.cfg.OBJECT.ROTATION_Y, rotate_z)
        
    def renderSettingHdri(self, hdri):
        # set hdri image
        self.env.image = bpy.data.images.load(os.path.join(self.hdri_dir, hdri))
    
    def renderSettingCamera(self, cam):
        bpy.context.scene.camera = cam


    def addRandomEffect(self):
        # random hdri strength
        hdri_strength = random.uniform(self.cfg.HDRI.STRENGTH_MIN, self.cfg.HDRI.STRENGTH_MAX)
        self.bg.inputs[1].default_value = hdri_strength

        # random spotlight strength
        spot_strength = random.uniform(self.cfg.LIGHT.STRENGTH_MIN, self.cfg.LIGHT.STRENGTH_MAX)
        bpy.data.lamps['Spot'].node_tree.nodes['Emission'].inputs[1].default_value = spot_strength

        # random spotlight shadow softness
        spot_softness = random.uniform(self.cfg.LIGHT.SHADOW_SOFT_MIN, self.cfg.LIGHT.SHADOW_SOFT_MAX)
        bpy.data.lamps['Spot'].shadow_soft_size = spot_softness

    def deleteMdl(self):
        bpy.ops.object.select_all(action='DESELECT')
        self.obj.select = True
        bpy.ops.object.delete()

    def renderShadowImg(self, img):
        bpy.ops.render.render()
        bpy.data.images['Render Result'].save_render(img)

    def renderNonShadowImg(self, img):
        bpy.ops.render.render()
        bpy.data.images['Render Result'].save_render(img)


    def setPath(self, root_dir):
        print('[ SETTING PATH ]')
        self.root_dir = root_dir
        self.mdl_dir = os.path.join(self.root_dir, 'mdl')
        self.doc_dir = os.path.join(self.root_dir, 'doc')
        self.hdri_dir = os.path.join(self.root_dir, 'hdri')
        self.out_dir = os.path.join(self.root_dir, 'out')
        self.shadow_dir = os.path.join(self.out_dir, 'shadow')
        self.non_shadow_dir = os.path.join(self.out_dir, 'non_shadow')

        mkdir_list = [self.out_dir, self.shadow_dir, self.non_shadow_dir]
        for d in mkdir_list:
            if not os.path.exists(d):
                os.makedirs(d)

    def getDocList(self):
        return sorted(os.listdir(self.doc_dir))

    def getMdlList(self):
        mdl_list = sorted(glob.glob(os.path.join(self.mdl_dir, '*.obj')))
        mdl_list = [os.path.basename(m) for m in mdl_list]
        return mdl_list

    def getHdriList(self):
        return sorted(os.listdir(self.hdri_dir))

    def getDocNum(self):
        return len(self.getDocList())

    def getMdlNum(self):
        return len(self.getMdlList())

    def getHdriNum(self):
        return len(self.getHdriList())

if __name__ == '__main__':
    args = get_args()
    cfg = get_cfg()
    br = BlenderRenderer(args.root_dir, cfg)
    nonShadowList, shadowList = br.renderAll(render_num=20)

