import time
import yt_dlp
import os
from mutagen.easyid3 import EasyID3
from ffmpeg import ffmpeg

from discord.ext import tasks

class Playlist ():
    def __init__(self):
        self.directory = 'Audio/' + str(id(self))
        self.index = 0
        self.starter = 0
        self.needle = 0
        self.prio = 0
        os.makedirs(self.directory)
        self.FFmpeg_executable = 'F:\Programming\drivers\FFMPEG/ffmpeg-4.4.1-essentials_build/bin/ffmpeg.exe'
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'windowsfilenames' : True,
            'lazy_playlist' : True,
            'restrictfilenames' : True,
            'ffmpeg_location': 'F:\Programming\drivers\FFMPEG/ffmpeg-4.4.1-essentials_build/bin/ffmpeg.exe',
            'outtmpl': 'Audio/' + str(id(self)) + '/' + '%(title)s.%(ext)s',
            'sleep_interval_subtitles': 2,
            'progress_hooks' : [self.__progress_hooks],
        }
    def set_ctx(self, ctx):
        self.ctx = ctx
    def set_channel(self,channel):
        self.channel = channel
    def set_voice(self,voice):
        self.voice = voice
    def set_player(self,player):
        self.player = player
    def set_discord(self,discord):
        self.discord = discord

    def __progress_hooks(self,response):
        if response["status"] == "finished" :
            self.video_path = response["filename"]
            video_title = self.video_path.split('\\')[2][:-5]
            os.rename('{}/{}.webm'.format(self.directory,video_title),'{}/{}&{}.webm'.format(self.directory,self.index,video_title))
            self.index += 1

    def file_list(self):
        lst = os.listdir(self.directory)
        value = sorted(lst, key=lambda x: int(x.split('&', 1)[0]))
        return value

    async def append(self,link):
            await self.__downloader(link)

    async def append_top(self,link):
            await self.__downloader(link)
            print(self.file_list())
            file = self.file_list()[-1]
            print(file)
            os.rename('{}/{}'.format(self.directory,file),'{}/{}1{}.webm'.format(self.directory,str(self.needle + 1),file[1:]))
            self.prio += 1



    async def __downloader(self,link):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            #info_dict = ydl.extract_info(link, download=False)
            #video_lenght = info_dict.get('duration',None)
            print("adding URL:" + link)
            ydl.download([link])

    @tasks.loop(seconds=2)
    async def listiner(self):
        if self.ctx.voice_client.is_playing():
                time.sleep(1)
        else:
            await self.play()


    def __del_audio(self,path):

        os.remove(self.directory + "/" + path)
    def __get_audio(self):
        index = self.starter
        fo = self.file_list()
        print(fo)
        try:
            if self.starter == 0:
                self.starter += 1
            print(fo[index])
            self.needle += 1
            return "{}/{}".format(self.directory, fo[index])
        except IndexError:
            print('expception thrown. index out of range \nque empty')
            if self.listiner.is_running():
                self.listiner.stop()
            return False




    async def play(self):
        fo = self.file_list()

        if not self.ctx.voice_client.is_playing():
            audio = self.__get_audio()
            if not audio :
                return
            else:
                source = self.discord.FFmpegOpusAudio(source=audio, executable=self.FFmpeg_executable)
                self.player.play(source=source,self=self.voice)
                if not self.listiner.is_running():
                    await self.listiner.start()
                if self.prio < 100:
                    self.prio += 1
                self.__del_audio(fo[0])