import os
import webbrowser
from utils import converttime, select_path, convertname, current_dir, check_ext

class VideoProcessor:
    def __init__(self):
        self.out_path = ""
        self.out_name = ""

    def download_video(self):
        video_link = input("Please paste the video link: ")
        print("\nDownloading original video: ")
        os.system(f'yt-dlp "{video_link}" --no-playlist --merge-output-format mp4 -o input.mp4')
        return check_ext("input.mp4")

    def process_full_video(self):
        self.out_name = input("\nType your output name, if blank, the name will be 'output.mp4': ")
        print("Please select the output directory, if you close the window, the video will be saved at the same directory as input.")
        self.out_path = select_path("Select the output directory: ")
        print("\nYour path: " + self.out_path)
        print("\nExporting...")
        os.system(f'ffmpeg.exe -v quiet -stats -i input.mp4 -c:v libx264 "{self.out_path}{convertname(self.out_name)}.mp4"')
        print("\nFinished exporting.")

    def process_cut_video(self):
        self.out_name = input("\nType your output name, if blank, the name will be 'output.mp4': ")
        print("Please select the output directory, if you close the window, the video will be saved at the same directory as input.")
        self.out_path = select_path("Select the output directory: ")
        print("\nYour path: " + self.out_path)
        if input('\nPress 1 to visualize video for cutting: ') == "1":
            print("Opening website on your default browser...")
            webbrowser.open("https://ytcutter.com/")
        begin = converttime(input("\nEnter the beginning time to cut: "))
        end = converttime(input("Enter the end time to cut: "))
        print("Video length is " + str(end - begin))
        print("Processing...")
        os.system(f'ffmpeg.exe -v quiet -stats -ss {begin} -t {end - begin} -i input.mp4 -y -c:v libx264 "{self.out_path}{convertname(self.out_name)}.mp4"')
        print("\nFinished exporting.")

    def cleanup(self):
        print("\nDeleting leftover input file")
        if check_ext("input.mp4"):
            os.system('del input.mp4 /s /q /f')
        if check_ext(".webm"):
            os.system('del *.webm /s /q /f')
        os.system("cls")

    def post_process(self):
        print("Finished.\n")
        if len(self.out_path) == 0:
            self.out_path = current_dir
        print("Exported video: " + self.out_path + convertname(self.out_name) + '.mp4\n')
        if input("Press 1 if you want to open the directory containing the output file: ") == "1":
            print("\nOpening the directory...")
            os.system('explorer ' + self.out_path.replace("/", "\\"))
        if input("\nPress 1 if you want to play the video using your default video player: ") == "1":
            print("\nOpening video file..")
            os.system(self.out_path + '"' + convertname(self.out_name) + '.mp4"')

    def run(self):
        if self.download_video():
            os.system("cls")
            print("""Please select between these options:
            1. Save the entire video
            2. Cut the video""")
            choice = input("\nInput your number here: ")
            if choice == '1':
                self.process_full_video()
            elif choice == '2':
                self.process_cut_video()
            else:
                print("Invalid choice. Exiting.")
                return
            self.cleanup()
            self.post_process()
            os.system('pause')
        else:
            print("\nCannot download video. Please try again.\n")
            os.system("pause")
