import bpy

import os
import sys
import glob
import json
import math
import random
import datetime
import argparse
import numpy as np
from easydict import EasyDict as edict
from PIL import Image


''' the script to automatively render batch of shadow and non-shadow paired images

Example usage:
    
    # asus pro
    ./blender -b --python /media/yslin/SSD_DATA/research/BlenderRender/src/blenderRenderer.py -- -r /media/yslin/SSD_DATA/research/BlenderRender -w WORKLOAD_0305_ASUS_PRO.json -g
    # csie server
    ./blender -b --python /nfs/inm_master/06/r06944059/BlenderRender/src/blenderRenderer.py -- -r /nfs/inm_master/06/r06944059/BlenderRender -w WORKLOAD_0305_CSIE10.json
    # cml server
    CUDA_VISIBLE_DEVICES=0 ./blender -b --python /tmp2/frank840306/research/BlenderRender/src/blenderRenderer.py -- -r /tmp2/frank840306/research/BlenderRender -w WORKLOAD_0305_CML26.json
    


'''
# sys.stdout = open('/tmp2/frank840306/research/BlenderRender/noise.log', w)
# _print = print
# file = open("/tmp2/frank840306/research/BlenderRender/noise.log", 'w+')
# def print(*args):
    # file.write(''.join(args))
    # _print(*args)

def print_file(*args):
    with open('/tmp2/frank840306/research/BlenderRender/out/output_large.log', 'a') as f:
    # with open('/media/yslin/SSD_DATA/research/BlenderRender/out/output.log', 'a') as f:
        print(*args, file=f)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root_dir', type=str, default='/media/yslin/SSD_DATA/research/BlenderRender', help='root directory')
    parser.add_argument('-w', '--workload', type=str, default='WORKLOAD_0305_ASUS_PRO.json', help='ex: WORKLOAD_0305_ASUS_PRO.json')
    parser.add_argument('-n', '--render_num', type=int, default=1, help='rendering number')
    parser.add_argument('-g', '--use_gpu', action='store_true', help='whether to use gpu or not')
    parser.add_argument('--ratio_range', type=float, nargs='+', default=[0.01, 0.9], help='the ratio range of mask to keep the pair')
    if '--' not in sys.argv:
        args = parser.parse_args()    
    else:
        argv = sys.argv[sys.argv.index('--') + 1:]
        args, _ = parser.parse_known_args(argv)
    return args

def get_cfg():
    __C = edict()

    cfg = __C

    # the camera
    __C.CAMERA = edict()
    __C.CAMERA.RESOLUTION_X = 1200
    __C.CAMERA.RESOLUTION_Y = 1600
    __C.CAMERA.PERCENTAGE = 100 # 100

    __C.CAMERA.SAMPLE = 512

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
    __C.OBJECT.LOCATION_Z = 15

    __C.OBJECT.ROTATION_X = math.pi * 90 / 180
    __C.OBJECT.ROTATION_Y = 0
    __C.OBJECT.ROTATION_Z = 0


    # __C.OBJECT.SCALE_X = 1
    # __C.OBJECT.SCALE_Y = 3
    # __C.OBJECT.SCALE_Z = 0.2

    __C.OBJECT.LOCATION_MIN = -0.8
    __C.OBJECT.LOCATION_MAX = 0.8

    __C.OBJECT.ROTATION_MIN = math.pi * 0 / 180
    __C.OBJECT.ROTATION_MAX = math.pi * 90 / 180


    # the hdri
    __C.HDRI = edict()
    __C.HDRI.STRENGTH_MIN = 0.01
    __C.HDRI.STRENGTH_MAX = 0.3


    # the light source
    __C.LIGHT = edict()
    __C.LIGHT.TYPE = 'SPOT'
    __C.LIGHT.ANGLE = math.pi * 45 / 180
    __C.LIGHT.SHADOW_SOFT_MIN = 0.1 
    __C.LIGHT.SHADOW_SOFT_MAX = 0.5
    
    __C.LIGHT.STRENGTH_MIN = 3000 # 3000 ~ 20000
    __C.LIGHT.STRENGTH_MAX = 10000 # 3000 ~ 20000


    __C.LIGHT.LOCATION_X = 0
    __C.LIGHT.LOCATION_Y = 0
    __C.LIGHT.LOCATION_Z = 22

    __C.LIGHT.LOCATION_MIN = -0.5
    __C.LIGHT.LOCATION_MAX = 0.5

    __C.LIGHT.ROTATION_X = 0
    __C.LIGHT.ROTATION_Y = 0 
    __C.LIGHT.ROTATION_Z = 0
    __C.LIGHT.COLOR = ['#FFC58F', '#FFF1E0', '#FFFFFF', '#C9E2FF']

    return cfg

def hexToRGBA(hex):
    gamma = 2.2
    hex = hex.lstrip('#')
    lv = len(hex)
    fin = list(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    r = pow(fin[0] / 255, gamma)
    g = pow(fin[1] / 255, gamma)
    b = pow(fin[2] / 255, gamma)
    fin.clear()
    fin.append(r)
    fin.append(g)
    fin.append(b)
    fin.append(1.0)
    return tuple(fin)

class BlenderRenderer(object):
    """docstring for BlenderRenderer"""
    def __init__(self, root_dir, workload, gpu, cfg):
        super(BlenderRenderer, self).__init__()
        self.setPath(root_dir)
        self.setWorkload(workload)
        
        self.cfg = cfg

        print_file('[ CONFIG ] # documents: {}, # 3d model: {}, # HDRI : {}'.format(self.doc_num, self.mdl_num, self.hdri_num))
        self.initEnv(gpu)
        
    def renderAll(self, render_num, ratio_range):
        total_num = self.doc_num * self.mdl_num * len(self.cameras) * render_num
        print_file('[ RENDER ] Total render num = {}'.format(total_num))
        
        nonShadowList = []
        shadowList = []
        # choose 1 document
        # choose 1 3d model
        # choose 1 HDRI
        
        total_cnt, doc_cnt = 0, 0
        start_time = datetime.datetime.now().strftime('%H:%M:%S')
        bgNonShadowImg = os.path.join(self.non_shadow_dir, 'bgNonShadow_{}.png'.format(start_time))
        bgShadowImg = os.path.join(self.shadow_dir, 'bgShadow_{}.png'.format(start_time))

        print_file('[ TIMESTAMP ] {}'.format(start_time))
        for doc in self.doc_list:
            
            cam_cnt = 0
            for cam in self.cameras:
                self.renderSettingCamera(cam)
                render_cnt = 0
                for idx in range(render_num):
                    
                    
                    mdl_cnt = 0
                    for mdl in self.mdl_list:
                        img_name = 'D{}M{}C{:02d}N{:05d}.png'.format(os.path.splitext(doc)[0], os.path.splitext(mdl)[0], cam_cnt+1, render_cnt+1)
                        print_file(' [ IMAGE ]: {}'.format(img_name))

                        # add hdri
                        hdri = random.choice(self.hdri_list)
                        self.renderSettingHdri(hdri)
                        
                        self.addRandomEffect()
                        nonShadowImg = os.path.join(self.non_shadow_dir, img_name)
                        shadowImg = os.path.join(self.shadow_dir, img_name)
                        maskImg = os.path.join(self.mask_dir, img_name)
                        
                        
                        # render background non-shadow
                        self.renderSettingDoc('background.png')
                        self.renderImg(bgNonShadowImg)
                        # render doc non-shadow
                        self.renderSettingDoc(doc)
                        nonShadowList.append(self.renderImg(nonShadowImg))
                        
                        self.renderSettingMdl(mdl)
                        # render background shadow
                        self.renderSettingDoc('background.png')
                        self.renderImg(bgShadowImg)
                        # render doc shadow
                        self.renderSettingDoc(doc)
                        shadowList.append(self.renderImg(shadowImg))
                        
                        if not self.obtainMask(bgNonShadowImg, bgShadowImg, maskImg, ratio_range):
                            os.remove(shadowImg)
                            os.remove(nonShadowImg)
                        self.deleteMdl()
                        print_file('\t[ Progress ] Total: [ {} / {} ], document: [ {} / {} ], 3D model: [ {} / {} ], camera: [ {} / {} ], render: [ {} / {} ]'.format(
                            total_cnt+1, total_num, doc_cnt+1, self.doc_num, mdl_cnt+1, self.mdl_num, cam_cnt+1, len(self.cameras), render_cnt+1, render_num))
                        mdl_cnt += 1
                        total_cnt += 1
                    render_cnt += 1
                cam_cnt += 1
            doc_cnt += 1
            print_file('[ TIMESTAMP ] {}'.format(datetime.datetime.now().strftime('%H:%M:%S')))
        
        os.remove(bgNonShadowImg)
        os.remove(bgShadowImg)
        print_file('[ RENDER ] Over')
        return nonShadowList, shadowList

    def initEnv(self, gpu):
        random.seed(840306)
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
        # self.cameras = [camera1, camera2, camera3, camera4, camera5]
        self.cameras = [camera1]
        # init render parameter
        bpy.data.scenes['Scene'].render.resolution_x = self.cfg.CAMERA.RESOLUTION_X
        bpy.data.scenes['Scene'].render.resolution_y = self.cfg.CAMERA.RESOLUTION_Y
        bpy.data.scenes['Scene'].render.resolution_percentage = self.cfg.CAMERA.PERCENTAGE
        bpy.data.scenes['Scene'].render.dither_intensity = self.dithering
        bpy.data.scenes['Scene'].cycles.samples = self.cfg.CAMERA.SAMPLE
        

        # set GPU or CPU
        scene = bpy.context.scene
        scene.cycles.device = 'GPU'

        prefs = bpy.context.user_preferences
        cprefs = prefs.addons['cycles'].preferences

        # Attempt to set GPU device types if available
        for compute_device_type in ('CUDA', 'OPENCL', 'NONE'):
            try:
                cprefs.compute_device_type = compute_device_type
                break
            except TypeError:
                pass

        # Enable all CPU and GPU devices
        for device in cprefs.devices:
            device.use = True

        # bpy.data.scenes['Scene'].cycles.device = 'GPU' if gpu else 'CPU'
        
        bpy.data.scenes['Scene'].render.layers[0].cycles.use_denoising = self.denoising

        # bpy.data.scenes['Scene'].render.layers[0].cycles.denoising_radius = 4
        # bpy.data.scenes['Scene'].render.layers[0].cycles.denoising_relative_pca = True
        
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
        # coord_z = random.uniform(self.cfg.OBJECT.LOCATION_Z_MIN, self.cfg.OBJECT.LOCATION_Z_MAX)
        rotate_z = random.uniform(self.cfg.OBJECT.ROTATION_MIN, self.cfg.OBJECT.ROTATION_MAX)
        
        self.obj.location = (coord_x, coord_y, self.cfg.OBJECT.LOCATION_Z)
        self.obj.rotation_euler = (self.cfg.OBJECT.ROTATION_X, self.cfg.OBJECT.ROTATION_Y, rotate_z)
        print_file('[ RANDOM MDL EFFECT ] coord: ({}, {}), rotate: {}'.format(coord_x, coord_y, rotate_z))


    def renderSettingHdri(self, hdri):
        # set hdri image
        self.env.image = bpy.data.images.load(os.path.join(self.hdri_dir, hdri))
    
    def renderSettingCamera(self, cam):
        bpy.context.scene.camera = cam


    def addRandomEffect(self):
        # random hdri strength
        hdri_strength = random.uniform(self.cfg.HDRI.STRENGTH_MIN, self.cfg.HDRI.STRENGTH_MAX)
        self.bg.inputs[1].default_value = hdri_strength
        # self.bg.inputs[1].default_value = self.cfg.HDRI.STRENGTH_MIN
        
        # random spotlight location
        spot_location_x = random.uniform(self.cfg.LIGHT.LOCATION_MIN, self.cfg.LIGHT.LOCATION_MAX)
        spot_location_y = random.uniform(self.cfg.LIGHT.LOCATION_MIN, self.cfg.LIGHT.LOCATION_MAX)
        bpy.data.objects['Spot'].location[0] = spot_location_x
        bpy.data.objects['Spot'].location[1] = spot_location_y
        
        # random spotlight strength
        spot_color = self.cfg.LIGHT.COLOR[random.choice(range(len(self.cfg.LIGHT.COLOR)))]
        spot_strength = random.uniform(self.cfg.LIGHT.STRENGTH_MIN, self.cfg.LIGHT.STRENGTH_MAX)
        bpy.data.lamps['Spot'].node_tree.nodes['Emission'].inputs[0].default_value = hexToRGBA(spot_color)
        bpy.data.lamps['Spot'].node_tree.nodes['Emission'].inputs[1].default_value = spot_strength
        # bpy.data.lamps['Spot'].node_tree.nodes['Emission'].inputs[1].default_value = self.cfg.LIGHT.STRENGTH_MIN
        

        # random spotlight shadow softness
        spot_softness = random.uniform(self.cfg.LIGHT.SHADOW_SOFT_MIN, self.cfg.LIGHT.SHADOW_SOFT_MAX)
        bpy.data.lamps['Spot'].shadow_soft_size = spot_softness
        print_file('[ RANDOM EFFECT ] \nhdri_strength: {}, spot_location: ({}, {}), spot_color: {}, spot_strength:{}, spot_softness: {}'.format(
            hdri_strength, spot_location_x, spot_location_y, spot_color, spot_strength, spot_softness
        ))


    def deleteMdl(self):
        bpy.ops.object.select_all(action='DESELECT')
        self.obj.select = True
        bpy.ops.object.delete()

    def obtainMask(self, N_img, S_img, M_img, ratio_range):
        N = np.array(Image.open(N_img).convert('L')).astype(np.float32)
        S = np.array(Image.open(S_img).convert('L')).astype(np.float32)
        
        M = N - S
        # print('M: ', M.shape)
        M[np.where(M < 0)] = 0

        if np.percentile(M, 99) < 20:
            print_file('[ PRUNE ] {} shallow shadow'.format(os.path.basename(N_img)))
            return False

        tmp_M = M.copy()[np.nonzero(M)]
        # tmp_M[np.nonzero(tmp_M)]
        # print('tmp_M: ', tmp_M)
        # print(tmp_M.shape)
        

        max_val = np.percentile(tmp_M, 80)
        min_val = np.percentile(tmp_M, 5)

        M[np.where(M > max_val)] = max_val
        M[np.where(M < min_val)] = min_val
        # print(np.max(M), max_val, min_val)
        M = 255 * (M - min_val) / (max_val - min_val)
        # M = M * 255 / max_val
        # M[np.where(M < 20)] = 0
        
        ratio = self.maskRatio(M)

        if ratio < ratio_range[0] or ratio > ratio_range[1]:
            print_file('[ PRUNE ] {} shadow ratio = {}'.format(os.path.basename(N_img), ratio))
            # os.remove(N_img)
            # os.remove(S_img)
            return False
        else:
            result = Image.fromarray(M.astype(np.uint8))
            result.save(M_img)
            return True

    def maskRatio(self, M):
        binary = np.zeros((self.cfg.CAMERA.RESOLUTION_Y, self.cfg.CAMERA.RESOLUTION_X), np.uint8)
        binary[np.where(M > 0)] = 1
        ratio = np.sum(binary) / (self.cfg.CAMERA.RESOLUTION_X * self.cfg.CAMERA.RESOLUTION_Y)
        return ratio

    def renderImg(self, img):
        bpy.ops.render.render()
        bpy.data.images['Render Result'].save_render(img)

    # def renderNonShadowImg(self, img):
    #     bpy.ops.render.render()
    #     bpy.data.images['Render Result'].save_render(img)


    def setPath(self, root_dir):
        print_file('[ SETTING PATH ]')
        self.root_dir = root_dir
        self.mdl_dir = os.path.join(self.root_dir, 'mdl')
        self.doc_dir = os.path.join(self.root_dir, 'doc')
        self.hdri_dir = os.path.join(self.root_dir, 'hdri')
        self.todo_dir = os.path.join(self.root_dir, 'todo')
        self.out_dir = os.path.join(self.root_dir, 'out')
        
    def setOutputPath(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.shadow_dir = os.path.join(self.dataset_dir, 'shadow')
        self.non_shadow_dir = os.path.join(self.dataset_dir, 'non_shadow')
        self.mask_dir = os.path.join(self.dataset_dir, 'mask')

        mkdir_list = [self.out_dir, self.dataset_dir, self.shadow_dir, self.non_shadow_dir, self.mask_dir]
        for d in mkdir_list:
            if not os.path.exists(d):
                os.makedirs(d)

    def setWorkload(self, workload=None):
        print_file('[ SETTING WORKLOAD ]')
        if workload and os.path.exists(os.path.join(self.todo_dir, workload)):
            with open(os.path.join(self.todo_dir, workload), 'r') as fp:
                settings = json.load(fp)
            self.doc_list = settings['doc']
            self.mdl_list = settings['mdl']
            self.hdri_list = settings['hdri']
            self.denoising = settings['param']['denoising']
            self.dithering = settings['param']['dithering']
            self.setOutputPath(os.path.join(self.out_dir, settings['param']['dataset']))
        else:
            self.doc_list = sorted(os.listdir(self.doc_dir))
            self.mdl_list = sorted(os.listdir(self.mdl_dir))
            self.hdri_list = sorted(os.listdir(self.hdri_dir))
            self.denoising = True
            self.dithering = 1
            self.setOutputPath(os.path.join(self.out_dir, 'Blender'))
        print_file('\t[ DOC ]: {}'.format(', '.join(self.doc_list)))
        print_file('\t[ MDL ]: {}'.format(', '.join(self.mdl_list)))
        print_file('\t[ hdri ]: {}'.format(', '.join(self.hdri_list)))
        print_file('\t[ DENOISING ]: {}'.format(self.denoising))
        print_file('\t[ DITHERING ]: {}'.format(self.dithering))
        print_file('\t[ DATASET ]: {}'.format(self.dataset_dir))
        self.doc_num = len(self.doc_list)
        self.mdl_num = len(self.mdl_list)
        self.hdri_num = len(self.hdri_list)
        return


if __name__ == '__main__':
    args = get_args()
    cfg = get_cfg()
    
    br = BlenderRenderer(args.root_dir, args.workload, args.use_gpu, cfg)
    nonShadowList, shadowList = br.renderAll(render_num=args.render_num, ratio_range=args.ratio_range)

    