'''
Created on 14/giu/2013

@author: ben
'''

import subprocess
import os
import time
import multiprocessing
import sys

import glob

class Converter(object):

    def __init__(self, path_to_ffmpeg = "ffmpeg", default_sampling = "44100", \
                 default_bitrate = "192k", default_format = ".mp3"):
        self.ffmpeg_path = path_to_ffmpeg
        self.default_sampling = default_sampling
        self.default_bitrate = default_bitrate
        self.default_format = default_format

    def __call__(self, file_name, new_format = "", bitrate = "", sampling = ""):
        self.convert(file_name, new_format, bitrate, sampling)

    def convert(self, file_name, new_format = "", bitrate = "", sampling = ""):
        if sampling == "":
            sampling = self.default_sampling
        if bitrate == "":
            bitrate = self.default_bitrate
        if new_format == "":
            new_format = self.default_format

        (base_name, ext) = os.path.splitext(file_name)
        new_name = base_name + new_format

        if os.path.exists(new_name):
            os.remove(new_name)

        cmd = [self.ffmpeg_path, "-i", file_name, "-ar", sampling, \
               "-ab", bitrate, "-ac", "2", new_name]
        subproc = subprocess.Popen(cmd, stderr=subprocess.PIPE)

        ret_code = subproc.poll()
        while ret_code is None:
            try:
                ret_code = subproc.poll()
                time.sleep(0.1)
            except KeyboardInterrupt:
                print("Terminating..")
                subproc.kill()
                break

        if ret_code > 0:
            raise ValueError(subproc.stderr.read())


class BatchConverter(object):

    def __init__(self, path_to_ffmpeg = "ffmpeg", default_sampling = "44100", \
                 default_bitrate = "192k"):
        self.conv = Converter(path_to_ffmpeg = path_to_ffmpeg, \
                              default_sampling = default_sampling, \
                              default_bitrate = default_bitrate)

    def convert(self, list_of_files, new_format):
        self.conv.default_format = new_format
        tot_files = len(list_of_files)

        pool = multiprocessing.Pool()
        mapper = pool.map_async(self.conv, list_of_files, 1)

        t = time.time()
        while not mapper.ready():
            left = mapper._number_left
            done = tot_files - left
            eta = left * (time.time() - t) / (done + (done == 0))
            sys.stdout.write("\rDone %04d/%04d (ETA: %2.1f s)" % (done, tot_files, eta))
            sys.stdout.flush()
            time.sleep(1)
        done = tot_files - mapper._number_left
        sys.stdout.write("\rDone %04d/%04d (in: %3.1f s)\n" % (done, tot_files, time.time() - t))
        sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) is not 3:
        raise ValueError("You should provide the source file name(s) " +
                         "(wildcards available), and destination format")

    list_of_files = glob.glob(sys.argv[1])
    multiconv = BatchConverter()
    multiconv.convert(list_of_files, sys.argv[2])



