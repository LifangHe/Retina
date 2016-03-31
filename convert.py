import h5py
import pickle
import numpy as np

image_text = pickle.load(open("image_text2.p","rb"))
imagecount = len(image_text)
print('list size of image text',imagecount)

laset=np.zeros((1,4))
print(laset.shape)
print(np.array([1,0,0,0]).shape)
imset=[]

for pair in image_text:
    for key in pair:
        if "Unable" in pair[key] or "unreadable" in pair[key]:
            imset.append(key)
            laset = np.append(laset,np.expand_dims(np.array([1,0,0,0]),axis=0), axis=0)

        elif "Severe" in pair[key] or "Significant retinopathy found" in pair[key]:
            imset.append(key)
            laset = np.append(laset, np.expand_dims(np.array([0,1,0,0]),axis=0), axis=0)

        elif "Mild" in pair[key] or "Minimal" in pair[key]:
            imset.append(key)
            laset = np.append(laset, np.expand_dims(np.array([0,0,1,0]),axis=0), axis=0)

        elif "No retinopathy found" in pair[key]:
            imset.append(key)
            laset = np.append(laset, np.expand_dims(np.array([0,0,0,1]),axis=0), axis=0)

print(laset.shape,laset[0])
laset = laset[1:]
print("laset ",laset.shape,'example',laset[0])
print("imset ",len(imset))

imgarray = np.zeros((37019,450, 600, 3))

print('imgarray',type(imgarray),imgarray.shape)

with h5py.File('label_name_array.h5', 'a') as FOB:
    FOB.attrs.create('count',0)
    FOB.create_dataset("labels",data=laset,compression="gzip", compression_opts=9)
    FOB.create_dataset("imagenames",data=imset,compression="gzip", compression_opts=9)
    FOB.create_dataset("imgarray",data=imgarray,compression="gzip",compression_opts=9)

print("SUCCESS!")
