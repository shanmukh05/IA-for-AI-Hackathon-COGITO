from pydub import AudioSegment
import os
import shutil
from tqdm import tqdm

MAINPATH = os.getcwd()
print(MAINPATH)

TRAIN_PATH = os.path.join(os.path.join(MAINPATH, "dataset"),"TrainAudioFiles")
TEST_PATH = os.path.join(os.path.join(MAINPATH, "dataset"),"TestAudioFiles")

TRAIN_FINAL = os.path.join(os.path.join(MAINPATH, "dataset"),"train")
TEST_FINAL = os.path.join(os.path.join(MAINPATH, "dataset"),"test")

TRAIN_LS = os.listdir(TRAIN_PATH)
TEST_LS = os.listdir(TEST_PATH)

print("Train : ", len(TRAIN_LS))
for f in tqdm(TRAIN_LS):
    if (f.split(".")[-1] == "wav"):
        shutil.copyfile(os.path.join(TRAIN_PATH,f),os.path.join(TRAIN_FINAL,f))
    else:
        sound = AudioSegment.from_mp3(os.path.join(TRAIN_PATH, f))
        name = f.split(".")[0] + ".wav"
        sound.export(os.path.join(TRAIN_FINAL, name), format="wav")

for f in tqdm(TEST_LS[1746:]):
    if (f.split(".")[-1] == "wav"):
        shutil.copyfile(os.path.join(TEST_PATH, f), os.path.join(TEST_FINAL, f))
    else:
        sound = AudioSegment.from_mp3(os.path.join(TEST_PATH, f))
        name = f.split(".")[0] + ".wav"
        sound.export(os.path.join(TEST_FINAL, name), format="wav")