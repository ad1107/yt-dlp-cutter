import os
import shutil
import webbrowser
from utils import converttime, select_path, convertname, current_dir, check_ext

class VideoProcessor:
    def __init__(self):
        self.out_path = ""
        self.out_name = ""

    # Video functions

    def download_video(self):
        video_link = input("Please paste the video link: ")
        print("\nDownloading original video: ")
        os.system(f'yt-dlp "{video_link}" --no-playlist --merge-output-format mp4 -o input.mp4')
        return check_ext("input.mp4")

    def process_full_video(self):
        self.out_name = input("\nType your output name, if blank, the name will be 'output.mp4': ")
        output_filename = convertname(self.out_name) + ".mp4"
        print("Please select the output directory, if you close the window, the video will be saved at the same directory as input.")
        self.out_path = select_path("Select the output directory: ")
        print("\nYour path: " + self.out_path)
        print("\nExporting...")

        input_file = "input.mp4"
        destination = os.path.join(self.out_path, output_filename)

        if input_file.lower().endswith(".mp4"):
            try:
                shutil.move(input_file, destination)
                print("\nFile moved to output directory.")
            except Exception as e:
                print("Error moving file:", e)
        else:
            # Otherwise, convert to MP4 using ffmpeg.
            os.system(f'ffmpeg.exe -v quiet -stats -i {input_file} -c:v libx264 "{destination}"')
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


    def download_audio(self):
        video_link = input("Please paste the video link for audio extraction: ")
        print("\nDownloading audio from the video: ")
        os.system(f'yt-dlp "{video_link}" --no-playlist --extract-audio --audio-format mp3 -o input_audio.mp3')
        return check_ext("input_audio.mp3")

    def process_full_audio(self):
        self.out_name = input("\nType your output name, if blank, the name will be 'output.mp3': ")
        output_filename = convertname(self.out_name) + ".mp3"
        print("Please select the output directory, if you close the window, the audio will be saved at the same directory as input.")
        self.out_path = select_path("Select the output directory: ")
        print("\nYour path: " + self.out_path)
        print("\nExporting...")
        input_file = "input_audio.mp3"
        destination = os.path.join(self.out_path, output_filename)
        # If the input file is already MP3, just move it.
        if input_file.lower().endswith(".mp3"):
            try:
                shutil.move(input_file, destination)
                print("\nFile moved to output directory.")
            except Exception as e:
                print("Error moving file:", e)
        else:
            os.system(f'ffmpeg.exe -v quiet -stats -i {input_file} -vn -y "{destination}"')
            print("\nFinished exporting.")

    def process_cut_audio(self):
        self.out_name = input("\nType your output name, if blank, the name will be 'output.mp3': ")
        print("Please select the output directory, if you close the window, the audio will be saved at the same directory as input.")
        self.out_path = select_path("Select the output directory: ")
        print("\nYour path: " + self.out_path)
        if input('\nPress 1 to visualize video for cutting: ') == "1":
            print("Opening website on your default browser...")
            webbrowser.open("https://ytcutter.com/")
        begin = converttime(input("\nEnter the beginning time to cut: "))
        end = converttime(input("Enter the end time to cut: "))
        print("Audio duration is " + str(end - begin))
        print("Processing...")
        os.system(f'ffmpeg.exe -v quiet -stats -ss {begin} -t {end - begin} -i input_audio.mp3 -y -vn -acodec libmp3lame "{self.out_path}{convertname(self.out_name)}.mp3"')
        print("\nFinished exporting.")

    # Cleanup functions

    def cleanup(self):
        print("\nDeleting leftover video file")
        if check_ext("input.mp4"):
            os.system('del input.mp4 /s /q /f')
        os.system("cls")

    def cleanup_audio(self):
        print("\nDeleting leftover audio file")
        if check_ext("input_audio.mp3"):
            os.system('del input_audio.mp3 /s /q /f')
        os.system("cls")

    # Post-processing functions

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

    def post_process_audio(self):
        print("Finished.\n")
        if len(self.out_path) == 0:
            self.out_path = current_dir
        print("Exported audio: " + self.out_path + convertname(self.out_name) + '.mp3\n')
        if input("Press 1 if you want to open the directory containing the output file: ") == "1":
            print("\nOpening the directory...")
            os.system('explorer ' + self.out_path.replace("/", "\\"))
        if input("\nPress 1 if you want to play the audio using your default audio player: ") == "1":
            print("\nOpening audio file..")
            os.system(self.out_path + '"' + convertname(self.out_name) + '.mp3"')

    # Main run function

    def run(self):
        print("Please select media type:")
        print("1. Video")
        print("2. Audio")
        media_choice = input("Input your choice: ")

        if media_choice == '1':
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
            else:
                print("\nCannot download video. Please try again.\n")
                os.system("pause")
                return

        elif media_choice == '2':
            if self.download_audio():
                os.system("cls")
                print("""Please select between these options:
1. Save the full audio
2. Cut the audio""")
                choice = input("\nInput your number here: ")
                if choice == '1':
                    self.process_full_audio()
                elif choice == '2':
                    self.process_cut_audio()
                else:
                    print("Invalid choice. Exiting.")
                    return
                self.cleanup_audio()
                self.post_process_audio()
            else:
                print("\nCannot download audio. Please try again.\n")
                os.system("pause")
                return
        else:
            print("Invalid media choice. Exiting.")
            return

        os.system('pause')
