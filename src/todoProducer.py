import json
import argparse
import datetime

'''
Example usages:
    python src/todoProducer.py -d 8 10 -m 1 7 -e 1 10 -f todo/WORKLOAD_0305_ASUS_PRO.json --dataset Blender40_residual
    
'''

DIGIT = {
    'doc': 4,
    'mdl': 3,
    'hdri': 3
}
EXT = {
    'doc': 'png',
    'mdl': 'obj',
    'hdri': 'hdr'
}

def get_args():
    date = datetime.datetime.now().strftime('%m%d')

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--doc', nargs='+', type=int, help='the range of document index')
    parser.add_argument('-m', '--mdl', nargs='+', type=int, default=[1, 7], help='the range of 3d model index')
    parser.add_argument('-e', '--hdri', nargs='+', type=int, default=[1, 10], help='the range of hdri image index')
    parser.add_argument('-f', '--file', type=str, default='WORDLOAD_{}.json'.format(date), help='produce the list file to render')
    parser.add_argument('--denoising', action='store_false', help='default to use denoising in Blender')
    parser.add_argument('--dithering', type=float, default=1, help='the value of dithering in Blender')
    parser.add_argument('--dataset', type=str, default='Blender', help='the name of dataset')
    args = parser.parse_args()
    return args

def make(cfg=None):
    print('{0} Script: todoProducer.py {0}'.format('=' * 20))
    print('[ CONFIG ]: {}'.format(cfg))

    settings = {'doc': [], 'mdl': [], 'hdri': []}
    
    for key in settings.keys():
        basename_format = '{' + ':0{}d'.format(DIGIT[key]) + '}'
        for idx in range(cfg[key][0], cfg[key][1] + 1):
            settings[key].append('{}.{}'.format(basename_format.format(idx), EXT[key]))
    settings['date'] = datetime.datetime.now().strftime('%Y.%m.%d')
    
    settings['param'] = {}
    settings['param']['denoising'] = cfg['denoising']
    settings['param']['dithering'] = cfg['dithering']
    settings['param']['dataset'] = cfg['dataset']
    
    with open(cfg['file'], 'w') as fp:
        json.dump(settings, fp, sort_keys=True, indent=4)

    print('WORKLOAD FILE: {}'.format(cfg['file']))
    print('{}'.format('=' * 65))

def main():
    args = get_args()
    make(cfg=vars(args))

if __name__ == "__main__":
    main()