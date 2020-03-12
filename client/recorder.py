from my_library import mThreading
import pyaudio as pa


class Recorder:
    def __init__(self, format=pa.paInt16, rate=44100):
        self.stream = pa.Stream(pa.PyAudio(), format=format, rate=rate, channels=2, input=True, output=True)

    def get_stream(self):
        return self.stream.read(4096)

    def audio_buffer(self):
        while True:
            yield self.get_stream()
            continue

    def play_alone(self, alone):
        self.stream.write(alone)


class ClientPlayer:
    def __init__(self, format=pa.paInt16, rate=44100):
        self.stream = pa.Stream(pa.PyAudio(), format=format, rate=rate, channels=2, input=True, output=True)
        self.buffer = []
        self.run()

    def add(self, buffer):
        self.buffer.append(buffer)

    @mThreading.thread
    def run(self):
        while True:
            for buffer in set(self.buffer):
                self.stream.write(buffer)
                self.buffer.remove(buffer)


if __name__ == '__main__':
    recorder = Recorder()
    for alone in recorder.audio_buffer():
        recorder.play_alone(alone)