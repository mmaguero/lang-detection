#utis.py
import tarfile
import glob
import dask.dataframe as dd

def untar_files(file, to_path='.'):
    tf = tarfile.open(file)
    tf.extractall(path=to_path)
    return True

def load_csv(path, sep=',', ext='csv'):
    if sep not in [',','\t']:
        print("Only csv or tsv")
        return
    files = glob.glob(path + "/*."+ext)
    frame = dd.read_csv(files, sep=sep)
    return frame
