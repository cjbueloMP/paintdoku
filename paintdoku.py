import argparse
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage import filters
from matplotlib.ticker import MultipleLocator



def create_paintdoku(image):
    #start with vertical columns
    xlists = []
    for i in range(image.shape[0]):
        line = image[i,:]
        listdata = make_groups(line)
        xlists.append(listdata)
    ylists = []
    for i in range(image.shape[1]):
        line = image[:,i]
        listdata = make_groups(line)
        ylists.append(listdata)
        
    return (xlists,ylists)
        
def make_groups(line):
    line = np.squeeze(line)
    groups = []
    subgroupnum = 0
    for pixel in line:
        if (pixel==1) and (subgroupnum>0):
            groups.append(subgroupnum)
            subgroupnum=0
        elif pixel==0:
            subgroupnum+=1
    if pixel==0:
        groups.append(subgroupnum)
    return groups

def make_list_hor_ticks(fig,ax,number,grouplist):
    numnums = len(grouplist)
    if numnums==0:
        return fig,ax
    offset = -1
    for i in range(numnums):
        ax.text(offset,number+.2,'{: >2}'.format(grouplist[i]))
        offset-=1
        
    return fig,ax

def make_list_vert_ticks(fig,ax,number,grouplist,basenum):
    numnums = len(grouplist)
    if numnums==0:
        return fig,ax
    offset = basenum
    for i in range(numnums):
        ax.text(number+.2,offset+.5,'{: >2}'.format(grouplist[i]))
        offset+=1
        
    return fig,ax


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('image',
                        type=str,
                        help='Image to make into a paintdoku')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()

    imagefile = args.image
 
    im = Image.open(imagefile).resize((45,60))
    im = np.array(im.convert('L'))
    val = filters.threshold_otsu(im)
    threshim = np.array(im>val).astype(int)
    [xlists,ylists] = create_paintdoku(threshim)
    #plt.imshow((im>val),cmap='gray')
    fig, ax = plt.subplots(1, figsize=(15, 18))
    ax.set_xlim((0,threshim.shape[1]))
    ax.set_ylim((0,threshim.shape[0]))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.set_yticklabels([])
    ax.set_xticklabels([])


    ax.set_aspect(1)
    plt.grid(b=True, which='major', color='#000000', linestyle='-')
    plt.grid(b=True, which='minor', color='#000000', linestyle='-', alpha=0.5)
    xlists.reverse()
    for i in range(len(xlists)):
        grouplist = xlists[i]
        grouplist.reverse()
        fig,ax = make_list_hor_ticks(fig,ax,i,grouplist)
    basenum = threshim.shape[0]
    for i in range(len(ylists)):
        grouplist = ylists[i]
        grouplist.reverse()
        fig,ax = make_list_vert_ticks(fig,ax,i,grouplist,basenum)
    plt.savefig('paintdoku.png',dpi=600)
    plt.figure()
    plt.imshow(threshim,cmap='gray')
    plt.savefig('solution.png')